"""Twilio WhatsApp webhook — full NeurOrientador conversation loop.

Receives inbound WhatsApp messages from Twilio (form-encoded POST),
runs the full pipeline, and replies via the Twilio REST API.

Pipeline per turn:
  1. Get or create patient (Supabase)
  2. Alarm filter — immediately escalate if keyword detected
  3. Build system prompt for current phase
  4. Call LLM (Claude / OpenRouter / OpenAI / Gemini)
  5. Parse and validate JSON response
  6. Score if phase == F3
  7. Determine next phase (PhaseRouter)
  8. Send WhatsApp reply via Twilio
  9. Persist updated patient state (Supabase)
  10. Audit log turn (Supabase — silently swallows errors)
"""

import logging
from typing import Optional

from fastapi import APIRouter, Request, Response

from app.alarm_filter import check_alarm
from app.audit_log import log_turno, update_historial
from app.json_guard import parse_and_validate
from app.llm_client import LLMClient
from app.phase_router import PhaseRouter
from app.schemas import Paciente
from app.scoring import process_f3_scoring
from app.supabase_repository import SupabaseRepository
from app.twilio_client import send_whatsapp_reply

logger = logging.getLogger(__name__)

webhook_router = APIRouter()

_TWIML_EMPTY = '<?xml version="1.0" encoding="UTF-8"?><Response></Response>'
_VERSION_PROMPT = "v6.0"

_MSG_ALARMA = (
    "🆘 Detectamos una posible emergencia. "
    "Por favor llama al 123 o acude a urgencias de inmediato. "
    "Nuestro equipo médico ha sido notificado."
)
_MSG_HUMANO = (
    "Estamos conectándote con un especialista del equipo ICN Salud. "
    "En breve te contactarán. Cuídate mucho."
)
_MSG_ADMIN = (
    "Para consultas sobre autorizaciones y trámites EPS, visita "
    "icnsalud.com o comunícate con nuestra línea administrativa."
)
_MSG_LLM_ERROR = (
    "Tenemos una dificultad técnica en este momento. "
    "Un especialista te contactará pronto."
)

# ── Lazy singletons (created once per worker process) ─────────────────────────

_repo: Optional[SupabaseRepository] = None
_llm: Optional[LLMClient] = None
_phase_router = PhaseRouter()


def _get_repo() -> SupabaseRepository:
    global _repo
    if _repo is None:
        _repo = SupabaseRepository()
    return _repo


def _get_llm() -> LLMClient:
    global _llm
    if _llm is None:
        _llm = LLMClient()
    return _llm


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_or_create_patient(telefono: str, repo: SupabaseRepository) -> Paciente:
    paciente = repo.get_paciente_by_telefono(telefono)
    if paciente is None:
        paciente = Paciente(
            paciente_id=f"PAC-{telefono[-8:]}",
            telefono=telefono,
            fase_actual="F0",
        )
        try:
            repo.create_paciente(paciente)
        except Exception:
            logger.exception("Could not persist new patient %s", telefono)
    return paciente


def _persist_patient_update(telefono: str, campos: dict, repo: SupabaseRepository) -> None:
    try:
        repo.update_paciente(telefono, campos)
    except Exception:
        logger.exception("Could not update patient %s", telefono)


# ── Webhook endpoint ──────────────────────────────────────────────────────────

@webhook_router.post("/twilio")
async def twilio_webhook(request: Request) -> Response:
    """Receive a Twilio WhatsApp message and reply via the Twilio REST API."""
    form = await request.form()
    from_raw = str(form.get("From", ""))
    body = str(form.get("Body", "")).strip()
    telefono = from_raw.replace("whatsapp:", "").strip()

    if not telefono or not body:
        return Response(content=_TWIML_EMPTY, media_type="text/xml")

    repo = _get_repo()
    paciente = _get_or_create_patient(telefono, repo)

    logger.info("Inbound [%s] fase=%s: %r", telefono, paciente.fase_actual, body[:80])

    # ── 1. Alarm filter ───────────────────────────────────────────────────────
    alarm_detected, keyword = check_alarm(body)
    if alarm_detected:
        logger.warning("ALARM detected for %s: %s", telefono, keyword)
        send_whatsapp_reply(telefono, _MSG_ALARMA)
        log_turno(
            paciente_id=paciente.paciente_id,
            telefono=telefono,
            fase=paciente.fase_actual,
            mensaje_usuario=body,
            respuesta_agente=_MSG_ALARMA,
            guia_soporte_turno=None,
            tokens_usados=0,
            flag_alarma=True,
            escalado_humano=True,
            version_prompt=_VERSION_PROMPT,
        )
        _persist_patient_update(telefono, {
            "fase_actual": "HUMANO",
            "requiere_humano": True,
            "motivo_escalamiento": f"Alarma detectada: {keyword}",
        }, repo)
        return Response(content=_TWIML_EMPTY, media_type="text/xml")

    # ── 2. LLM call ───────────────────────────────────────────────────────────
    system_prompt = _phase_router.get_system_prompt(paciente.fase_actual, paciente)
    try:
        raw_response, tokens_usados = _get_llm().call(
            system_prompt, paciente.historial_json, body
        )
    except Exception:
        logger.exception("LLM call failed for %s", telefono)
        send_whatsapp_reply(telefono, _MSG_LLM_ERROR)
        return Response(content=_TWIML_EMPTY, media_type="text/xml")

    # ── 3. Parse & validate JSON ──────────────────────────────────────────────
    response_ia = parse_and_validate(raw_response)
    error_json = response_ia is None
    if error_json:
        logger.warning("JSON parse failed for %s — raw: %r", telefono, raw_response[:200])

    # ── 4. Scoring (F3 only) ──────────────────────────────────────────────────
    score_result = None
    if not error_json and paciente.fase_actual == "F3":
        score_result = process_f3_scoring(response_ia.puntaje_dominio)

    # ── 5. Next phase ─────────────────────────────────────────────────────────
    next_phase = _phase_router.get_next_phase(
        paciente, response_ia, score_result, error_json
    )

    # ── 6. Build reply text ───────────────────────────────────────────────────
    if error_json:
        respuesta = _MSG_LLM_ERROR
    elif next_phase == "HUMANO":
        visible = response_ia.respuesta_visible
        respuesta = f"{visible}\n\n{_MSG_HUMANO}" if visible else _MSG_HUMANO
    elif next_phase == "ADMIN":
        visible = response_ia.respuesta_visible
        respuesta = f"{visible}\n\n{_MSG_ADMIN}" if visible else _MSG_ADMIN
    else:
        respuesta = response_ia.respuesta_visible

    # ── 7. Send reply ─────────────────────────────────────────────────────────
    send_whatsapp_reply(telefono, respuesta)

    # ── 8. Persist patient state ──────────────────────────────────────────────
    historial = update_historial(paciente, body, respuesta)
    campos: dict = {
        "fase_actual": next_phase,
        "historial_json": historial,
    }
    if score_result:
        campos["nivel_riesgo"] = score_result.get("nivel_riesgo")
        campos["score_total"] = score_result.get("score_total", 0)
    if next_phase == "HUMANO":
        campos["requiere_humano"] = True
    if response_ia and response_ia.guia_soporte:
        campos["guia_soporte"] = response_ia.guia_soporte
    if response_ia and response_ia.cie10:
        campos["cie10"] = response_ia.cie10

    _persist_patient_update(telefono, campos, repo)

    # ── 9. Audit log ──────────────────────────────────────────────────────────
    log_turno(
        paciente_id=paciente.paciente_id,
        telefono=telefono,
        fase=paciente.fase_actual,
        mensaje_usuario=body,
        respuesta_agente=respuesta,
        guia_soporte_turno=response_ia.guia_soporte if response_ia else None,
        tokens_usados=tokens_usados,
        flag_alarma=False,
        escalado_humano=(next_phase == "HUMANO"),
        version_prompt=_VERSION_PROMPT,
    )

    logger.info("Turn done [%s] %s → %s", telefono, paciente.fase_actual, next_phase)
    return Response(content=_TWIML_EMPTY, media_type="text/xml")
