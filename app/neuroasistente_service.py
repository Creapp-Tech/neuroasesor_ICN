"""NeuroAsistente service — post-agenda patient accompaniment.

Handles the four-step follow-up flow for patients with scheduled appointments:
  1. Appointment confirmation (immediate)
  2. Preparation instructions (day before or shortly after confirmation)
  3. Reminder (1 day before the appointment)
  4. Post-consultation follow-up (1 day AFTER the appointment)

Every interaction is persisted in NEUROASISTENTE_INTERACCIONES so the Neuroasesor
can review and supervise. Clinical or commercial signals in patient responses
trigger an escalation to the Neuroasesor.

Architecture note: this module uses Supabase (via SupabaseRepository) and the
WhatsApp/ManyChat clients from specs 2 and 7. It deliberately avoids
escalation_service.py which is based on the old SQLAlchemy stack.
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from app import config
from app.manychat_client import assign_to_human, update_contact_tag
from app.schemas import (
    Cita,
    Escalamiento,
    NeuroAsistenteInteraccion,
    Paciente,
)
from app.supabase_repository import SupabaseRepository
from app.whatsapp_client import send_message

logger = logging.getLogger(__name__)

# Lazy-initialised singleton — avoids connecting to Supabase at import time
_repo: Optional[SupabaseRepository] = None


def _get_repo() -> SupabaseRepository:
    global _repo
    if _repo is None:
        _repo = SupabaseRepository()
    return _repo


# ── Keyword tables for analyze_response ──────────────────────────────────────

_CLINICAL_SIGNALS = [
    "me duele más", "duele más", "empeoro", "empeor", "peor que antes",
    "complicaci", "efecto secundario", "reacci", "medicament", "pastilla",
    "dosis", "fiebre", "vómito", "vomito", "mareo", "convulsi",
    "angustia", "miedo", "ansiedad", "desesperado", "no aguanto",
    "me siento mal", "me siento peor",
]

_COMMERCIAL_SIGNALS = [
    "cancelar", "cancelo", "no voy a ir", "no puedo ir", "no iré",
    "reagendar", "cambiar la cita", "cambiar fecha",
    "nuevo programa", "otro programa", "interesado en", "quiero más información",
    "inconform", "molest", "mal servicio", "queja", "reclamo",
    "no me sirvió", "no quedé satisfecho", "no me gustó",
]


# ── Internal helpers ──────────────────────────────────────────────────────────

def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _make_interaccion_id(paciente_id: str) -> str:
    ts = _now_utc().strftime("%Y%m%dT%H%M%S")
    short = str(uuid.uuid4())[:8]
    return f"NA-{paciente_id}-{ts}-{short}"


def _build_and_send(
    paciente: Paciente,
    cita: Cita,
    tipo_interaccion: str,
    mensaje: str,
) -> NeuroAsistenteInteraccion:
    """Send a WhatsApp message and persist the interaction record."""
    enviado = send_message(paciente.telefono, mensaje)
    estado = "enviado" if enviado else "pendiente"

    interaccion = NeuroAsistenteInteraccion(
        interaccion_id=_make_interaccion_id(paciente.paciente_id),
        paciente_id=paciente.paciente_id,
        cita_id=cita.cita_id,
        fecha_hora=_now_utc(),
        canal_contacto="whatsapp",
        tipo_interaccion=tipo_interaccion,
        mensaje_enviado=mensaje,
        estado_interaccion=estado,
        requiere_revision_clinica=False,
        requiere_revision_comercial=False,
        responsable="NeuroAsistente_automatico",
        prioridad_paciente=paciente.prioridad_operativa,
        version_flujo=config.VERSION_FLUJO,
    )

    try:
        _get_repo().insert_neuroasistente_interaccion(interaccion)
    except Exception:
        logger.exception("Error persisting NeuroAsistente interaction %s", interaccion.interaccion_id)

    return interaccion


# ── Public send functions ─────────────────────────────────────────────────────

def send_confirmacion_cita(paciente: Paciente, cita: Cita) -> NeuroAsistenteInteraccion:
    """Send appointment confirmation immediately after scheduling."""
    nombre = paciente.nombre or "paciente"
    fecha = cita.fecha_cita.strftime("%d/%m/%Y") if cita.fecha_cita else "a confirmar"
    hora = cita.hora_cita or "a confirmar"
    programa = cita.programa or paciente.programa_clinico or "Neurología"

    mensaje = (
        f"Hola {nombre} 👋 Queremos confirmarte tu cita con ICN Salud:\n\n"
        f"📅 Fecha: {fecha}\n"
        f"🕐 Hora: {hora}\n"
        f"📋 Programa: {programa}\n\n"
        "¿Confirmas tu asistencia? Responde SÍ o NO. "
        "Si necesitas cambiar la fecha, también puedes decírnoslo aquí."
    )
    return _build_and_send(paciente, cita, "confirmacion_cita", mensaje)


def send_preparacion_cita(paciente: Paciente, cita: Cita) -> NeuroAsistenteInteraccion:
    """Send preparation instructions based on the clinical programme."""
    nombre = paciente.nombre or "paciente"
    programa = cita.programa or paciente.programa_clinico or "neurológico"

    mensaje = (
        f"Hola {nombre} 👋 Tu cita con ICN Salud se acerca. "
        "Antes de venir, te compartimos algunas recomendaciones:\n\n"
        f"Para tu programa de *{programa}*:\n"
        "• Llega 10 minutos antes\n"
        "• Trae tu documento de identidad y tarjeta de salud\n"
        "• Si tomas medicamentos, tráelos o anota sus nombres\n"
        "• Si tienes estudios previos relacionados, tráelos también\n\n"
        "¿Tienes alguna pregunta? Estamos aquí para ayudarte 🙂"
    )
    return _build_and_send(paciente, cita, "preparacion_cita", mensaje)


def send_recordatorio(paciente: Paciente, cita: Cita) -> NeuroAsistenteInteraccion:
    """Send a warm reminder 1 day before the appointment."""
    nombre = paciente.nombre or "paciente"
    hora = cita.hora_cita or "la hora acordada"

    mensaje = (
        f"Hola {nombre} 👋 Te recordamos que mañana tienes cita con ICN Salud "
        f"a las *{hora}*. ¡Te esperamos! "
        "Si necesitas algo antes de tu consulta, escríbenos cuando quieras."
    )
    return _build_and_send(paciente, cita, "recordatorio", mensaje)


def send_seguimiento_post_cita(paciente: Paciente, cita: Cita) -> NeuroAsistenteInteraccion:
    """Send post-consultation follow-up 1 day AFTER the appointment date."""
    nombre = paciente.nombre or "paciente"

    mensaje = (
        f"Hola {nombre} 👋 ¿Cómo te fue ayer en tu consulta con el neurólogo? "
        "Queremos saber cómo estás y si quedaste con alguna duda o necesitas ayuda "
        "con algo. Estamos aquí para acompañarte 🙂"
    )
    return _build_and_send(paciente, cita, "seguimiento_post_cita", mensaje)


# ── Response analysis ─────────────────────────────────────────────────────────

def analyze_response(respuesta: str, tipo_interaccion: str) -> tuple[bool, bool]:
    """
    Classify a patient response into clinical and/or commercial signals.

    Returns:
        (requiere_revision_clinica, requiere_revision_comercial)
    """
    texto = respuesta.lower()
    clinica = any(signal in texto for signal in _CLINICAL_SIGNALS)
    comercial = any(signal in texto for signal in _COMMERCIAL_SIGNALS)
    return clinica, comercial


# ── Response processing ───────────────────────────────────────────────────────

def process_patient_response(interaccion_id: str, respuesta: str) -> None:
    """
    Record the patient's reply, analyse for signals, and escalate if needed.

    Loads the interaction from Supabase, updates estado=respondido and
    respuesta_paciente, then triggers escalation when clinical or commercial
    signals are detected.
    """
    repo = _get_repo()
    interaccion = repo.get_neuroasistente_interaccion_by_id(interaccion_id)

    if interaccion is None:
        logger.error("Interaction not found: %s", interaccion_id)
        return

    clinica, comercial = analyze_response(respuesta, interaccion.tipo_interaccion)

    campos: dict = {
        "respuesta_paciente": respuesta,
        "estado_interaccion": "respondido",
        "requiere_revision_clinica": clinica,
        "requiere_revision_comercial": comercial,
    }
    repo.update_neuroasistente_interaccion(interaccion_id, campos)

    # Persist updated values locally for escalation
    interaccion.respuesta_paciente = respuesta
    interaccion.requiere_revision_clinica = clinica
    interaccion.requiere_revision_comercial = comercial

    if clinica:
        tipo_esc = "neuroasistente_clinico"
        logger.info("Clinical signal detected in interaction %s — escalating", interaccion_id)
        _trigger_escalamiento(interaccion, tipo_esc)
    elif comercial:
        tipo_esc = "neuroasistente_comercial"
        logger.info("Commercial signal detected in interaction %s — escalating", interaccion_id)
        _trigger_escalamiento(interaccion, tipo_esc)


def handle_no_response(interaccion_id: str, horas_sin_respuesta: int) -> None:
    """
    Manage interactions with no patient reply.

    24 h without response  → estado = pendiente
    72 h without response  → estado = cerrado, notas = "sin respuesta tras 2 intentos"
    """
    repo = _get_repo()

    if horas_sin_respuesta >= 72:
        campos = {
            "estado_interaccion": "cerrado",
            "notas_internas": "sin respuesta tras 2 intentos",
        }
        logger.info("Interaction %s closed after 72h with no response", interaccion_id)
    elif horas_sin_respuesta >= 24:
        campos = {"estado_interaccion": "pendiente"}
        logger.info("Interaction %s marked pending after 24h with no response", interaccion_id)
    else:
        return  # Not enough time elapsed to change state

    try:
        repo.update_neuroasistente_interaccion(interaccion_id, campos)
    except Exception:
        logger.exception("Error updating no-response state for %s", interaccion_id)


# ── Escalation ────────────────────────────────────────────────────────────────

def _trigger_escalamiento(
    interaccion: NeuroAsistenteInteraccion,
    tipo: str,
) -> None:
    """
    Create an Escalamiento record and notify the Neuroasesor.

    Uses Supabase directly (avoids the SQLAlchemy-based escalation_service).
    tipo: "neuroasistente_clinico" | "neuroasistente_comercial"
    """
    repo = _get_repo()
    ts = _now_utc()
    escalamiento_id = f"ESC-{interaccion.paciente_id}-{ts.strftime('%Y%m%dT%H%M%S')}"

    escalamiento = Escalamiento(
        escalamiento_id=escalamiento_id,
        paciente_id=interaccion.paciente_id,
        timestamp_escalamiento=ts,
        tipo_escalamiento=tipo,
        prioridad_paciente=interaccion.prioridad_paciente,
        fase_origen="NeuroAsistente",
        motivo=(
            f"Señal {'clínica' if 'clinico' in tipo else 'comercial'} detectada "
            f"en interacción {interaccion.tipo_interaccion}. "
            f"Respuesta paciente: {interaccion.respuesta_paciente or '—'}"
        ),
    )

    try:
        repo.insert_escalamiento(escalamiento)
    except Exception:
        logger.exception("Error persisting escalamiento %s", escalamiento_id)

    # Tag patient in ManyChat and notify Neuroasesor via WhatsApp
    try:
        update_contact_tag(interaccion.paciente_id, "escalado")
        assign_to_human(interaccion.paciente_id, interaccion.prioridad_paciente)
    except Exception:
        logger.exception("ManyChat error during escalation for %s", interaccion.paciente_id)

    _notify_neuroasesor(interaccion, tipo)


def _notify_neuroasesor(interaccion: NeuroAsistenteInteraccion, tipo: str) -> None:
    """Send WhatsApp notification to the Neuroasesor."""
    tipo_label = "CLÍNICO" if "clinico" in tipo else "COMERCIAL"
    mensaje = (
        f"🔔 *REVISIÓN {tipo_label} — NeuroAsistente*\n"
        f"Paciente ID: {interaccion.paciente_id}\n"
        f"Tipo interacción: {interaccion.tipo_interaccion}\n"
        f"Respuesta: {interaccion.respuesta_paciente or '—'}\n"
        f"Interacción ID: {interaccion.interaccion_id}\n\n"
        "Por favor revisa y actúa según protocolo."
    )
    try:
        send_message(config.ICN_NEUROASESOR_WHATSAPP, mensaje)
    except Exception:
        logger.exception("Error notifying Neuroasesor for interaction %s", interaccion.interaccion_id)


# ── Public escalation entry point (called by spec 9 tasks) ───────────────────

def trigger_escalamiento_neuroasistente(
    interaccion: NeuroAsistenteInteraccion,
    paciente: Paciente,
    tipo: str,
) -> None:
    """
    Public wrapper — matches the signature expected by spec 9 tasks.
    tipo: "neuroasistente_clinico" | "neuroasistente_comercial"
    """
    _trigger_escalamiento(interaccion, tipo)
