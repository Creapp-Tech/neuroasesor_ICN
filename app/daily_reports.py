"""Daily reports — NeuroAsistente daily summary generation and delivery.

Generates the daily operational summary at 8:00 PM Colombia time, Monday to
Saturday. Aggregates NEUROASISTENTE_INTERACCIONES and ESCALAMIENTOS metrics,
produces a narrative via LLM, and sends the result to the Neuroasesor by
WhatsApp, then persists in RESUMENES_DIARIOS.
"""

import logging
from datetime import date, datetime
from typing import Optional

from app import config
from app.schemas import ResumenDiario
from app.supabase_repository import SupabaseRepository
from app.whatsapp_client import send_message

logger = logging.getLogger(__name__)

COLOMBIA_TZ = config.COLOMBIA_TZ

_repo: Optional[SupabaseRepository] = None


def _get_repo() -> SupabaseRepository:
    global _repo
    if _repo is None:
        _repo = SupabaseRepository()
    return _repo


def _generate_narrative(metricas: dict) -> str:
    """Generate a narrative summary using the LLM. Falls back to empty string on error."""
    try:
        from app.llm_client import LLMClient
        client = LLMClient()
        prompt = (
            "Genera un resumen ejecutivo del día del NeuroAsistente con estos datos. "
            "Tono: operativo, claro, directo. "
            "Incluye alertas si hay casos clínicos o comerciales pendientes.\n\n"
            f"Datos del día:\n{metricas}"
        )
        text, _ = client.call(
            system_prompt="Eres el asistente de reportes de NeurOrientador ICN Salud.",
            historial=[],
            mensaje_actual=prompt,
        )
        return text or "Resumen no disponible."
    except Exception:
        logger.exception("Error generating narrative with LLM")
        return "Resumen narrativo no disponible."


def generate_daily_summary(fecha: Optional[date] = None) -> ResumenDiario:
    """Generate a daily summary from NeuroAsistente interactions for the given date.

    If fecha is None, uses today's date in Colombia timezone.
    """
    if fecha is None:
        fecha = datetime.now(COLOMBIA_TZ).date()

    repo = _get_repo()
    interacciones = repo.get_interacciones_del_dia(fecha)
    escalamientos = repo.get_escalamientos_del_dia(fecha)

    total = len(interacciones)
    respondidas = sum(1 for i in interacciones if i.estado_interaccion == "respondido")
    sin_respuesta = sum(1 for i in interacciones if i.estado_interaccion == "cerrado")
    clinicas = sum(1 for i in interacciones if i.requiere_revision_clinica)
    comerciales = sum(1 for i in interacciones if i.requiere_revision_comercial)
    total_esc = len(escalamientos)

    esc_con_sla = [e for e in escalamientos if e.cumple_sla_15min is not None]
    sla_pct = (
        100.0 * sum(1 for e in esc_con_sla if e.cumple_sla_15min) / len(esc_con_sla)
        if esc_con_sla
        else 0.0
    )

    tiempos = [
        e.tiempo_respuesta_humano
        for e in escalamientos
        if e.tiempo_respuesta_humano is not None
    ]
    tiempo_prom = sum(tiempos) / len(tiempos) if tiempos else 0.0

    metricas = {
        "fecha": str(fecha),
        "total_interacciones": total,
        "respondidas": respondidas,
        "sin_respuesta": sin_respuesta,
        "clinicas": clinicas,
        "comerciales": comerciales,
        "escalamientos": total_esc,
        "sla_pct": round(sla_pct, 1),
        "tiempo_prom_min": round(tiempo_prom, 1),
    }

    narrativo = _generate_narrative(metricas)

    return ResumenDiario(
        resumen_id=f"RES-{fecha.isoformat()}",
        fecha=fecha,
        total_interacciones_na=total,
        total_respondidas=respondidas,
        total_sin_respuesta=sin_respuesta,
        casos_revision_clinica=clinicas,
        casos_revision_comercial=comerciales,
        total_escalamientos=total_esc,
        sla_cumplido_pct=round(sla_pct, 1),
        tiempo_respuesta_promedio=round(tiempo_prom, 1),
        resumen_narrativo=narrativo,
    )


def send_daily_summary(resumen: ResumenDiario) -> None:
    """Format the daily summary and send it to the Neuroasesor via WhatsApp.

    Always persists the ResumenDiario to RESUMENES_DIARIOS regardless of
    whether the WhatsApp delivery succeeds.
    """
    ts = datetime.now(COLOMBIA_TZ).strftime("%d/%m/%Y %H:%M")
    respondidas_pct = (
        round(100.0 * resumen.total_respondidas / resumen.total_interacciones_na)
        if resumen.total_interacciones_na > 0
        else 0
    )

    mensaje = (
        f"📊 *RESUMEN DEL DÍA — NEUROASISTENTE · ICN Salud*\n"
        f"Fecha: {resumen.fecha.strftime('%d/%m/%Y')}  ·  Generado: {ts}\n\n"
        f"*ACTIVIDAD DEL DÍA*\n"
        f"• Total de pacientes contactados: {resumen.total_interacciones_na}\n"
        f"• Pacientes que respondieron: {resumen.total_respondidas} ({respondidas_pct}%)\n"
        f"• Sin respuesta: {resumen.total_sin_respuesta}\n\n"
        f"*⚠️ REQUIEREN ATENCIÓN*\n"
        f"• Revisión clínica: {resumen.casos_revision_clinica}\n"
        f"• Revisión comercial: {resumen.casos_revision_comercial}\n"
        f"• Sin respuesta >24h: {resumen.total_sin_respuesta}\n\n"
        f"*SLA*: {resumen.sla_cumplido_pct}% cumplido · "
        f"Tiempo prom: {resumen.tiempo_respuesta_promedio} min\n\n"
        f"📝 {resumen.resumen_narrativo or 'Sin resumen narrativo.'}"
    )

    try:
        send_message(config.ICN_NEUROASESOR_WHATSAPP, mensaje)
    except Exception:
        logger.exception("Error sending daily summary WhatsApp message")

    try:
        _get_repo().insert_resumen_diario(resumen)
    except Exception:
        logger.exception("Error persisting daily summary %s", resumen.resumen_id)


def _run_daily_summary() -> None:
    """Internal runner invoked by the scheduler."""
    try:
        resumen = generate_daily_summary()
        send_daily_summary(resumen)
    except Exception:
        logger.exception("Error in scheduled daily summary run")


def schedule_daily_summary() -> None:
    """Start the APScheduler job: 8:00 PM Colombia, Monday to Saturday."""
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger

        scheduler = BackgroundScheduler(timezone=COLOMBIA_TZ)
        scheduler.add_job(
            _run_daily_summary,
            CronTrigger(hour=20, minute=0, day_of_week="mon-sat", timezone=COLOMBIA_TZ),
            id="daily_summary",
            replace_existing=True,
        )
        scheduler.start()
        logger.info("Daily summary scheduler started — 8:00 PM Colombia, Mon–Sat")
    except Exception:
        logger.exception("Failed to start daily summary scheduler")
