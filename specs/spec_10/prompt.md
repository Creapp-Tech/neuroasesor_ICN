# Prompt — Spec 10: neuroasesor_service.py + daily_reports.py

Eres un Ingeniero de Backend Python con experiencia en sistemas operativos de salud. Tu tarea es implementar el registro del Neuroasesor y la generación del resumen diario automático para NeurOrientador de ICN Salud.

## Contexto
El Neuroasesor es el punto de control humano del sistema. Todo lo que hace debe quedar registrado. El resumen diario del NeuroAsistente se genera a las 8:00 PM Colombia (lunes a sábado) y se envía al Neuroasesor para supervisión. Los specs anteriores ya están implementados.

## Entrega requerida

### Archivo 1: `neuroasesor_service.py`
```python
def register_intervencion(
    paciente_id: str,
    tipo: str,  # de los valores Literal de NeuroAsesorInteraccion
    canal: str,
    resumen: str,
    resultado: str,
    responsable: str,
    oportunidad_detectada: Optional[str] = None,
    incidencia: Optional[str] = None,
    notas_internas: Optional[str] = None
) -> NeuroAsesorInteraccion:
    """
    Registra intervención del Neuroasesor en NEUROASESOR_INTERACCIONES.
    neuroasesor_interaccion_id = f"NA_H-{paciente_id}-{timestamp_iso}"
    prioridad_paciente copiada del paciente.
    """

def record_escalamiento_atendido(escalamiento_id: str, neuroasesor: str) -> None:
    """
    Registra que el Neuroasesor atendió el escalamiento.
    Llama escalation_service.register_human_response(escalamiento_id)
    Crea interacción tipo=escalamiento_clinico o comercial.
    """
```

### Archivo 2: `daily_reports.py`
```python
def generate_daily_summary() -> ResumenDiario:
    """
    1. Filtrar NEUROASISTENTE_INTERACCIONES del día (fecha_hora)
    2. Calcular métricas:
       - total_interacciones_na
       - total_respondidas (estado=respondido)
       - total_sin_respuesta (estado=cerrado, respuesta_paciente="sin_respuesta")
       - casos_revision_clinica (requiere_revision_clinica=True)
       - casos_revision_comercial (requiere_revision_comercial=True)
       - total_escalamientos (del día en ESCALAMIENTOS)
       - sla_cumplido_pct (% con cumple_sla_15min=True)
       - tiempo_respuesta_promedio
    3. Generar resumen_narrativo con LLM
    4. Crear y retornar ResumenDiario
    """

def send_daily_summary(resumen: ResumenDiario) -> None:
    """
    Formatear según plantilla y enviar al Neuroasesor por WhatsApp.
    Insertar en RESUMENES_DIARIOS.
    """

def schedule_daily_summary() -> None:
    """
    Configurar ejecución automática a las 8:00 PM Colombia, lunes-sábado.
    Usar APScheduler con COLOMBIA_TZ.
    """
```

## Plantilla del resumen diario (del documento V6 Documento 5)
```
📊 RESUMEN DEL DÍA — NEUROASISTENTE · ICN Salud
Fecha: [fecha]  ·  Generado: [timestamp]

ACTIVIDAD DEL DÍA
• Total de pacientes contactados: [N]
• Total de mensajes enviados: [N]
• Pacientes que respondieron: [N] ([%]%)
• Sin respuesta: [N]

TIPOS DE INTERACCIÓN
• Confirmaciones: [N] | Preparaciones: [N] | Recordatorios: [N] | Seguimientos: [N]

⚠️ REQUIEREN ATENCIÓN
• Revisión clínica: [N] — [lista nombres y señal]
• Revisión comercial: [N] — [lista nombres y oportunidad]
• Sin respuesta >24h: [N] — [lista nombres]
```
