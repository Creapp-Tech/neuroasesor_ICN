"""NeuroAsesor service — human Neuroasesor intervention registry.

Handles registration of direct Neuroasesor interventions in NEUROASESOR_INTERACCIONES
and records when escalations are attended to update SLA compliance metrics.

Architecture note: bypasses the SQLAlchemy-based escalation_service.py and uses
SupabaseRepository directly, consistent with the rest of the v6 stack.
"""

import logging
from datetime import datetime, timezone
from typing import Optional

from app import config
from app.schemas import NeuroAsesorInteraccion
from app.supabase_repository import SupabaseRepository

logger = logging.getLogger(__name__)

_repo: Optional[SupabaseRepository] = None


def _get_repo() -> SupabaseRepository:
    global _repo
    if _repo is None:
        _repo = SupabaseRepository()
    return _repo


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def register_intervencion(
    paciente_id: str,
    tipo: str,
    canal: str,
    resumen: str,
    resultado: str,
    responsable: str,
    oportunidad_detectada: Optional[str] = None,
    incidencia: Optional[str] = None,
    notas_internas: Optional[str] = None,
) -> NeuroAsesorInteraccion:
    """Register a Neuroasesor intervention in NEUROASESOR_INTERACCIONES.

    neuroasesor_interaccion_id format: NA_H-{paciente_id}-{timestamp_iso}
    """
    ts = _now_utc()
    interaccion_id = f"NA_H-{paciente_id}-{ts.strftime('%Y%m%dT%H%M%S')}"

    interaccion = NeuroAsesorInteraccion(
        neuroasesor_interaccion_id=interaccion_id,
        paciente_id=paciente_id,
        fecha_hora_inicio=ts,
        canal=canal,
        tipo_interaccion=tipo,
        resumen_conversacion=resumen,
        resultado=resultado,
        responsable=responsable,
        oportunidad_detectada=oportunidad_detectada,
        incidencia=incidencia,
        notas_internas=notas_internas,
    )

    try:
        _get_repo().insert_neuroasesor_interaccion(interaccion)
    except Exception:
        logger.exception("Error persisting NeuroAsesor interaction %s", interaccion_id)

    return interaccion


def record_escalamiento_atendido(escalamiento_id: str, neuroasesor: str) -> None:
    """Record that the Neuroasesor attended an escalation.

    Updates the escalamiento with response timestamp and SLA compliance,
    then creates a NeuroAsesor intervention record.
    """
    repo = _get_repo()
    ts_respuesta = _now_utc()

    try:
        esc = repo.get_escalamiento_by_id(escalamiento_id)
    except Exception:
        logger.exception("Error fetching escalamiento %s", escalamiento_id)
        return

    if esc is None:
        logger.error("Escalamiento not found: %s", escalamiento_id)
        return

    tiempo_min = (ts_respuesta - esc.timestamp_escalamiento).total_seconds() / 60.0
    sla_limite = (
        config.SLA_ALARMA_MINUTOS
        if esc.tipo_escalamiento == "alarma_critica"
        else config.SLA_MINUTOS
    )
    cumple_sla = tiempo_min <= sla_limite

    campos = {
        "timestamp_respuesta_humano": ts_respuesta.isoformat(),
        "tiempo_respuesta_humano": round(tiempo_min, 2),
        "cumple_sla_15min": cumple_sla,
        "responsable": neuroasesor,
    }

    try:
        repo.update_escalamiento(escalamiento_id, campos)
    except Exception:
        logger.exception("Error updating escalamiento %s", escalamiento_id)

    tipo_interaccion = (
        "escalamiento_clinico"
        if "clinico" in esc.tipo_escalamiento or "alarma" in esc.tipo_escalamiento
        else "escalamiento_comercial"
    )

    register_intervencion(
        paciente_id=esc.paciente_id,
        tipo=tipo_interaccion,
        canal="whatsapp",
        resumen=(
            f"Escalamiento {escalamiento_id} atendido. "
            f"Tiempo de respuesta: {round(tiempo_min, 1)} min. "
            f"SLA {'cumplido' if cumple_sla else 'incumplido'}."
        ),
        resultado="cerrado",
        responsable=neuroasesor,
    )
