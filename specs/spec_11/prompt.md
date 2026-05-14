# Prompt — Spec 11: audit_log.py

Eres un Ingeniero de Backend Python con experiencia en sistemas de salud auditables. Tu tarea es implementar la capa de trazabilidad para NeurOrientador de ICN Salud.

## Contexto
Todo lo que hace el sistema debe quedar registrado. Cada turno de conversación se guarda en la tabla CONVERSACIONES con trazabilidad clínica (guia_soporte del turno, version_prompt, tokens, flag_alarma). El historial_json en PACIENTES se mantiene truncado a MAX_HISTORIAL_TURNOS para controlar costos de tokens. Se almacena como JSONB en PostgreSQL.

## Entrega requerida: `audit_log.py`

```python
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
    version_prompt: str
) -> Conversacion:
    """
    Registra turno en CONVERSACIONES.
    conv_id = f"CONV-{paciente_id}-{timestamp_iso}"
    timestamp en timezone Colombia.
    """

def update_historial(
    paciente: Paciente, 
    mensaje_usuario: str, 
    respuesta_agente: str
) -> list:
    """
    Agrega turno al historial_json del paciente.
    Si len(historial) > config.MAX_HISTORIAL_TURNOS: eliminar el más antiguo.
    Formato de cada turno: {"role": "user"|"assistant", "content": str}
    Retorna historial actualizado como lista Python (sin serializar).
    """

def log_error_operativo(
    paciente_id: str, 
    descripcion: str, 
    tipo: str  # "json_invalido" | "api_error" | "db_error" | etc.
) -> None:
    """
    Registra error en logging Python (nivel ERROR).
    Actualiza campo error_operativo del paciente en PACIENTES si es persistente.
    """

def get_conversaciones_paciente(paciente_id: str) -> List[Conversacion]:
    """Retorna todas las conversaciones de un paciente para auditoría."""
```

## Regla de historial (del documento Sección 5, Make paso 12)
- Máximo 20 turnos en historial_json
- Al agregar turno: si len > MAX_HISTORIAL_TURNOS → eliminar el elemento [0] (más antiguo)
- El historial se almacena como JSONB en PostgreSQL; SQLAlchemy lo maneja como lista Python nativamente (sin serialización manual)

## Formato de salida
Archivo `audit_log.py` completo y limpio.
