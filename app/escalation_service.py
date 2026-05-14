"""Escalation service for NeurOrientador.

Handles human escalation workflows with SLA tracking, notifications, and breach handling.
"""

import logging
from datetime import datetime, timezone
from typing import Optional

import httpx
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base, engine
from .models.patient import Patient
from .config import (
    ICN_NEUROASESOR_WHATSAPP,
    ICN_COORDINADOR_WHATSAPP,
    SLA_MINUTOS,
    SLA_ALARMA_MINUTOS,
    TZ,
)
from .whatsapp_client import send_message as whatsapp_send
from .manychat_client import assign_to_human, mark_as_vencida

logger = logging.getLogger(__name__)

# ─── Model: Escalamiento ────────────────────────────────────────────────
class Escalamiento(Base):
    """
    Tabla para registrar escalamientos humanos con SLA.
    """
    __tablename__ = "escalamientos"

    id = Column(Integer, primary_key=True, index=True)
    escalamiento_id = Column(String(50), unique=True, nullable=False)
    paciente_id = Column(String(30), ForeignKey("pacientes.paciente_id"), nullable=False)
    tipo = Column(String(50))  # 'alarma_critica', 'clinico', 'comercial', etc.
    motivo = Column(Text)
    fase_origen = Column(String(10))
    timestamp_escalamiento = Column(DateTime(timezone=True), server_default=func.now())
    timestamp_respuesta_humano = Column(DateTime(timezone=True), nullable=True)
    tiempo_respuesta_humano = Column(Integer, nullable=True)  # minutos
    cumple_sla_15min = Column(Boolean, default=False)
    notas_clinicas = Column(Text)

    # Relación con paciente (opcional, para joins)
    paciente = relationship("Patient", foreignkeys=[paciente_id])

# ─── Functions ───────────────────────────────────────────────────────────

def create_escalamiento(
    paciente: Patient,
    tipo: str,
    motivo: str,
    fase_origen: str,
) -> Escalamiento:
    """
    Crea registro de escalamiento en ESCALAMIENTOS.
    escalamiento_id = f"ESC-{paciente.paciente_id}-{timestamp_iso}"
    prioridad_paciente copiada de paciente.prioridad_operativa
    """
    from .database import SessionLocal

    db = SessionLocal()
    try:
        # Generar timestamp ISO para el ID
        timestamp_iso = datetime.now(timezone.utc).isoformat()
        escalamiento_id = f"ESC-{paciente.paciente_id}-{timestamp_iso}"

        # Crear instancia
        escalamiento = Escalamiento(
            escalamiento_id=escalamiento_id,
            paciente_id=paciente.paciente_id,
            tipo=tipo,
            motivo=motivo,
            fase_origen=fase_origen,
        )

        db.add(escalamiento)
        db.commit()
        db.refresh(escalamiento)
        return escalamiento
    finally:
        db.close()


def notify_neuroasesor(
    escalamiento: Escalamiento,
    paciente: Patient,
    notas_clinicas: str,
) -> None:
    """
    Notifica al Neuroasesor con TODOS los datos obligatorios:
    Nombre, teléfono, problema principal, nivel_riesgo,
    resumen clínico, motivo, prioridad, fase_origen.

    Enviar por WhatsApp a config.ICN_NEUROASESOR_WHATSAPP.
    Llamar manychat_client.assign_to_human() con la prioridad.
    """
    # Construir mensaje
    message_body = (
        f"🚨 **NUEVO ESCALAMIENTO**\n"
        f"📌 Paciente: {paciente.nombre or 'Desconocido'}\n"
        f"📞 Teléfono: {paciente.telefono}\n"
        f"⚠️ Problema: {escalamiento.motivo}\n"
        f"📊 Riesgo: {paciente.nivel_riesgo or 'Desconocido'}\n"
        f"📝 Notas clínicas: {notas_clinicas}\n"
        f"🎯 Motivo: {escalamiento.tipo}\n"
        f"🔖 Prioridad: {escalamiento.tipo}\n"
        f"🔄 Fase origen: {escalamiento.fase_origen}\n"
        "\nPor favor, responda a esta message vía WhatsApp o a través del panel de ManyChat."
    )

    # Enviar WhatsApp al Neuroasesor
    whatsapp_send(ICN_NEUROASESOR_WHATSAPP, message_body)

    # Asignar conversación en ManyChat con la prioridad
    assign_to_human(paciente.telefono, escalamiento.tipo)


def register_human_response(escalamiento_id: str) -> float:
    """
    Registra que el Neuroasesor respondió.
    timestamp_respuesta_humano = now() Colombia timezone
    tiempo_respuesta_humano = minutos transcurridos desde timestamp_escalamiento
    Actualiza registro en ESCALAMIENTOS.
    Llama check_sla_compliance() y retorna minutos.
    """
    from .database import SessionLocal
    from datetime import datetime, timezone
    import pytz

    db = SessionLocal()
    try:
        escalamiento = db.query(Escalamiento).filter_by(escalamiento_id=escalamiento_id).first()
        if not escalamiento:
            logger.error("Escalamiento no encontrado: %s", escalamiento_id)
            return -1.0

        # Timestamp actual en zona horaria Colombia
        colombia_tz = pytz.timezone(TZ)
        now_colombia = datetime.now(colombia_tz)
        escalamiento.timestamp_respuesta_humano = now_colombia

        # Calcular tiempo de respuesta en minutos
        time_diff = now_colombia - escalamiento.timestamp_escalamiento.replace(tzinfo=timezone.utc)
        minutos = time_diff.total_seconds() / 60
        escalamiento.tiempo_respuesta_humano = minutos

        # Verificar SLA
        cumple_sla = check_sla_compliance(escalamiento)
        escalamiento.cumple_sla_15min = cumple_sla

        db.add(escalamiento)
        db.commit()
        db.refresh(escalamiento)
        return minutos
    finally:
        db.close()


def check_sla_compliance(escalamiento: Escalamiento) -> bool:
    """
    Calcula cumple_sla_15min según tipo.
    Actualiza campo en ESCALAMIENTOS.
    Si False: llama handle_sla_breach().
    """
    # Determinar umbral SLA según tipo
    if escalamiento.tipo == "alarma_critica":
        sla_threshold = SLA_ALARMA_MINUTOS  # 5 minutos
    elif escalamiento.tipo == "neuroasistente_comercial":
        sla_threshold = 30  # 30 minutos según prompt
    else:
        sla_threshold = SLA_MINUTOS  # 15 minutos por defecto

    # Verificar si el tiempo de respuesta es menor o igual al umbral
    if escalamiento.tiempo_respuesta_humano is None:
        return False  # No hay respuesta aún

    cumple = escalamiento.tiempo_respuesta_humano <= sla_threshold
    escalamiento.cumple_sla_15min = cumple

    # Si no cumple, manejar incumplimiento
    if not cumple:
        handle_sla_breach(escalamiento)

    return cumple


def handle_sla_breach(escalamiento: Escalamiento) -> None:
    """
    Acciones ante SLA incumplido:
    1. Registrar cumple_sla_15min=False en ESCALAMIENTOS
    2. Alertar coordinador ICN (config.ICN_COORDINADOR_WHATSAPP)
    3. manychat_client.mark_as_vencida(paciente.telefono)
    4. Registrar incidencia (para resumen diario)
    """
    from .database import SessionLocal

    db = SessionLocal()
    try:
        # Obtener paciente
        paciente = db.query(Patient).filter_by(paciente_id=escalamiento.paciente_id).first()
        if not paciente:
            logger.error("Paciente no encontrado para escalamiento: %s", escalamiento.escalamiento_id)
            return

        # 1. Actualizar registro de escalamiento (ya se hizo en check_sla_compliance)
        # 2. Alertar coordinador ICN
        message_body = (
            f"⚠️ **INCIDENTE SLA**\n"
            f"📌 Paciente: {paciente.nombre or 'Desconocido'}\n"
            f"📞 Teléfono: {paciente.telefono}\n"
            f"🚨 Escalamiento: {escalamiento.tipo}\n"
            f"⏱️ Tiempo respuesta: {escalamiento.tiempo_respuesta_humano:.1f} min\n"
            f"❌ SLA incumplido (umbral: {SLA_MINUTOS if escalamiento.tipo != 'alarma_critica' else SLA_ALARMA_MINUTOS} min)\n"
            "\nPor favor, revise el sistema y contacte al paciente si es necesario."
        )
        whatsapp_send(ICN_COORDINADOR_WHATSAPP, message_body)

        # 3. Marcar conversación como vencida en ManyChat
        mark_as_vencida(paciente.telefono)

        # 4. Registrar incidencia (podría ser un log en la base de datos)
        logger.warning("SLA breach for %s: %s", paciente.telefono, escalamiento.tipo)

    finally:
        db.close()


def trigger_alarm_escalamiento(
    paciente: Patient,
    motivo_alarma: str,
    notas: str,
) -> Escalamiento:
    """
    Flujo completo para alarma clínica crítica:
    1. NO llamar al LLM (ya validado en alarm_filter)
    2. Enviar al paciente mensaje de orientación a urgencias + datos ICN
    3. Crear escalamiento tipo=alarma_critica
    4. Notificar Neuroasesor inmediatamente
    5. Retornar escalamiento creado
    """
    from .database import SessionLocal

    # 2. Mensaje al paciente
    patient_message = (
        "⚠️ Por la urgencia de lo que describes, te recomendamos acudir a urgencias de inmediato o llamar a la línea de emergencias. "
        f"Un asesor de ICN Salud también fue notificado y te contactará en los próximos minutos. "
        f"Contacto ICN: {ICN_NEUROASESOR_WHATSAPP}"
    )
    whatsapp_send(paciente.telefono, patient_message)

    # 3. Crear escalamiento de tipo alarma_critica
    escalamiento = create_escalamiento(
        paciente=paciente,
        tipo="alarma_critica",
        motivo=motivo_alarma,
        fase_origen=paciente.fase_actual,
    )

    # 4. Notificar Neuroasesor inmediatamente
    notify_neuroasesor(escalamiento, paciente, notas)

    return escalamiento