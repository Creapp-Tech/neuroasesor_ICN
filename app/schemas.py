"""Pydantic models for NeurOrientador.

Only data definitions – no business logic. Fields match the V6 specification
exactly, using Optional where a value may be absent.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel


class Paciente(BaseModel):
    """Model representing a patient (PACIENTES table)."""
    # Required identifiers
    paciente_id: str
    telefono: str

    # Demographics — absent for brand-new patients
    nombre: Optional[str] = None
    edad: Optional[int] = None
    ciudad: Optional[str] = None
    aseguramiento: Optional[str] = None
    entidad_prepagada: Optional[str] = None

    # Consent
    consentimiento_datos_clinicos: bool = False
    consentimiento_teleorientacion: bool = False
    consentimiento_investigacion: bool = False
    timestamp_consentimiento: Optional[datetime] = None

    # Flow state
    fase_actual: Literal["F0", "F1", "F2", "F3", "F4", "ADMIN", "HUMANO"] = "F0"
    tipo_consulta: Optional[str] = None
    programa_clinico: Optional[str] = None
    problema_seleccionado: Optional[int] = None  # INTEGER in DB
    guia_soporte: Optional[str] = None
    cie10: Optional[str] = None

    # Clinical scoring
    nivel_riesgo: Optional[Literal["Bajo", "Moderado", "Alto", "Alarma"]] = None
    score_total: int = 0
    fenotipo_probable: Optional[str] = None
    respuestas_orientacion: Optional[dict] = None  # JSONB object

    # Agenda / conversion
    reporte_enviado: bool = False
    conversion: Optional[str] = None
    fecha_cita: Optional[date] = None
    canal_agenda: Optional[str] = None
    estado_cita: Optional[str] = None
    fecha_primera_orientacion: Optional[date] = None
    fecha_ultima_orientacion: Optional[date] = None
    cohorte: Optional[str] = None

    # Escalation / errors
    requiere_humano: bool = False
    requiere_revision_medica: bool = False
    motivo_escalamiento: Optional[str] = None
    error_json: bool = False
    error_operativo: Optional[str] = None

    # Versioning & audit
    version_prompt: Optional[str] = None
    version_flujo: str = "v6.0"
    historial_json: list = []  # JSONB array — no manual serialization
    notas_internas: Optional[str] = None
    prioridad_operativa: Literal["agendado", "particular", "general"] = "general"
    fecha_creacion: Optional[datetime] = None
    ultima_actividad: Optional[datetime] = None


class Conversacion(BaseModel):
    """Model representing a conversation turn."""
    conv_id: str
    paciente_id: str
    telefono: str
    fase: str
    mensaje_usuario: str
    respuesta_agente: str
    guia_soporte_turno: Optional[str] = None
    timestamp: datetime
    tokens_usados: int = 0
    flag_alarma: bool = False
    escalado_humano: bool = False
    version_prompt: Optional[str] = None


class Cita(BaseModel):
    """Model representing an appointment."""
    cita_id: str
    paciente_id: str
    tipo: str
    programa: str
    fecha_cita: date
    hora_cita: Optional[str] = None
    canal_agenda: Optional[str] = None
    confirmacion: Optional[str] = None
    seguimiento_post: bool = False
    resultado_post: Optional[str] = None


class Escalamiento(BaseModel):
    """Model representing a human escalation."""
    escalamiento_id: str
    paciente_id: str
    timestamp_escalamiento: datetime
    timestamp_respuesta_humano: Optional[datetime] = None
    tiempo_respuesta_humano: Optional[float] = None
    cumple_sla_15min: Optional[bool] = None
    tipo_escalamiento: Literal[
        "alarma_critica",
        "clinico",
        "comercial",
        "solicitud_paciente",
        "error_sistema",
        "neuroasistente_clinico",
        "neuroasistente_comercial",
    ]
    prioridad_paciente: Literal["agendado", "particular", "general"] = "general"
    fase_origen: Optional[str] = None
    motivo: str
    resolucion: Optional[str] = None
    responsable: Optional[str] = None
    resultado: Optional[str] = None


class NeuroAsistenteInteraccion(BaseModel):
    """Model representing an interaction from NeuroAsistente."""
    interaccion_id: str
    paciente_id: str
    cita_id: Optional[str] = None
    fecha_hora: datetime
    canal_contacto: str
    tipo_interaccion: Literal[
        "confirmacion_cita",
        "preparacion_cita",
        "recordatorio",
        "seguimiento_post_cita",
        "resolucion_duda",
        "acompañamiento",
        "oportunidad_comercial",
    ]
    mensaje_enviado: str
    respuesta_paciente: Optional[str] = None
    estado_interaccion: Literal["enviado", "respondido", "pendiente", "cerrado", "escalado"] = "enviado"
    requiere_revision_clinica: bool = False
    requiere_revision_comercial: bool = False
    notas_internas: Optional[str] = None
    responsable: Literal["NeuroAsistente_automatico", "Neuroasesor_humano", "Sistema_Make"]
    accion_generada: Optional[str] = None
    prioridad_paciente: Literal["agendado", "particular", "general"] = "general"
    version_flujo: str = "v6.0"
    timestamp_actualizacion: Optional[datetime] = None


class NeuroAsesorInteraccion(BaseModel):
    """Model representing an interaction from Neuroasesor."""
    neuroasesor_interaccion_id: str
    paciente_id: str
    fecha_hora_inicio: datetime
    fecha_hora_fin: Optional[datetime] = None
    tiempo_respuesta_humano: Optional[float] = None
    cumple_sla_15min: Optional[bool] = None
    canal: str
    tipo_interaccion: Literal[
        "escalamiento_clinico",
        "escalamiento_comercial",
        "supervision_neuroasistente",
        "contacto_proactivo",
        "soporte",
        "cierre_comercial",
    ]
    prioridad_paciente: Literal["agendado", "particular", "general"] = "general"
    resumen_conversacion: Optional[str] = None
    resultado: Literal[
        "cerrado",
        "pendiente",
        "escalado_medico",
        "nueva_cita_agendada",
        "rechazo",
        "sin_respuesta",
    ]
    oportunidad_detectada: Optional[str] = None
    incidencia: Optional[str] = None
    notas_internas: Optional[str] = None
    responsable: str
    version_flujo: str = "v6.0"


class ResumenDiario(BaseModel):
    """Model representing a daily management summary."""
    resumen_id: str
    fecha: date
    total_interacciones_na: int = 0
    total_respondidas: int = 0
    total_sin_respuesta: int = 0
    casos_revision_clinica: int = 0
    casos_revision_comercial: int = 0
    total_escalamientos: int = 0
    sla_cumplido_pct: float = 0.0
    tiempo_respuesta_promedio: float = 0.0
    total_interacciones_neuroasesor: int = 0
    resumen_narrativo: Optional[str] = None
    incidencias_sla: int = 0
    oportunidades_detectadas: int = 0


class ResponseIA(BaseModel):
    """Model representing the strict JSON output from the AI model."""
    respuesta_visible: str
    notas_internas: str
    puntaje_dominio: Dict[str, int]  # keys D1 to D6
    guia_soporte: Optional[str] = None
    cie10: Optional[str] = None
