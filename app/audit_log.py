"""Audit log — full traceability for NeurOrientador.

Records every conversation turn in CONVERSACIONES with clinical metadata
(guia_soporte, version_prompt, tokens, flag_alarma). Maintains the patient's
historial_json capped at MAX_HISTORIAL_TURNOS. Logs operational errors both
to Python logging and to the patient's error_operativo field in PACIENTES.
"""

import logging
from datetime import datetime
from typing import List, Optional

from app import config
from app.schemas import Conversacion, Paciente
from app.supabase_repository import SupabaseRepository

logger = logging.getLogger(__name__)

COLOMBIA_TZ = config.COLOMBIA_TZ

_repo: Optional[SupabaseRepository] = None


def _get_repo() -> SupabaseRepository:
    global _repo
    if _repo is None:
        _repo = SupabaseRepository()
    return _repo


def _now_colombia() -> datetime:
    return datetime.now(COLOMBIA_TZ)


def log_turno(
    paciente_id: str,
    telefono: str,
    fase: str,
    mensaje_usuario: str,
    respuesta_agente: str,
    guia_soporte_turno: Optional[str],
    tokens_usados: int,
    flag_alarma: bool,
    escalado_humano: bool,
    version_prompt: str,
) -> Conversacion:
    """Register a conversation turn in CONVERSACIONES.

    conv_id format: CONV-{paciente_id}-{timestamp_colombia}
    Timestamp uses Colombia timezone.
    """
    ts = _now_colombia()
    conv_id = f"CONV-{paciente_id}-{ts.strftime('%Y%m%dT%H%M%S')}"

    conv = Conversacion(
        conv_id=conv_id,
        paciente_id=paciente_id,
        telefono=telefono,
        fase=fase,
        mensaje_usuario=mensaje_usuario,
        respuesta_agente=respuesta_agente,
        guia_soporte_turno=guia_soporte_turno,
        timestamp=ts,
        tokens_usados=tokens_usados,
        flag_alarma=flag_alarma,
        escalado_humano=escalado_humano,
        version_prompt=version_prompt,
    )

    try:
        _get_repo().insert_conversacion(conv)
    except Exception:
        logger.exception("Error persisting conversacion %s", conv_id)

    return conv


def update_historial(
    paciente: Paciente,
    mensaje_usuario: str,
    respuesta_agente: str,
) -> list:
    """Add a user+assistant turn to the patient's historial_json.

    Each turn appends two entries: {"role": "user", ...} and {"role": "assistant", ...}.
    Trims from the oldest entry while len > MAX_HISTORIAL_TURNOS.
    Returns the updated list without mutating the original.
    """
    historial = list(paciente.historial_json)
    historial.append({"role": "user", "content": mensaje_usuario})
    historial.append({"role": "assistant", "content": respuesta_agente})

    while len(historial) > config.MAX_HISTORIAL_TURNOS:
        historial.pop(0)

    return historial


def log_error_operativo(
    paciente_id: str,
    descripcion: str,
    tipo: str,
) -> None:
    """Log an operational error and persist it to the patient record.

    tipo examples: "json_invalido", "api_error", "db_error"
    """
    logger.error(
        "Operational error [%s] for patient %s: %s",
        tipo,
        paciente_id,
        descripcion,
    )

    try:
        _get_repo().update_paciente_by_id(
            paciente_id,
            {"error_operativo": f"[{tipo}] {descripcion}"},
        )
    except Exception:
        logger.exception(
            "Failed to persist error_operativo for patient %s", paciente_id
        )


def get_conversaciones_paciente(paciente_id: str) -> List[Conversacion]:
    """Return all conversation turns for a patient (for quality audit)."""
    try:
        return _get_repo().get_conversaciones_by_paciente_id(paciente_id)
    except Exception:
        logger.exception(
            "Error fetching conversaciones for patient %s", paciente_id
        )
        return []
