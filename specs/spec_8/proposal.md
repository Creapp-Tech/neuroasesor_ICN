# Spec 8 — escalation_service.py: Servicio de Escalamiento y SLA

## Qué resuelve
Implementa el protocolo de escalamiento humano con medición automática de SLA. Notifica al Neuroasesor con los datos obligatorios del escalamiento (nombre, teléfono, problema, riesgo, resumen clínico, motivo, prioridad, fase). Calcula `tiempo_respuesta_humano` y `cumple_sla_15min`. Registra incumplimientos y alerta al coordinador ICN.

## Por qué es necesaria
El documento (Secciones 12-14, V6 Documentos 2 y 7) define el SLA de 15 minutos como KPI obligatorio medido automáticamente. Los escalamientos sin los datos completos no son válidos. El incumplimiento de SLA debe registrarse, alertar al coordinador y marcar la conversación como vencida en ManyChat.

## Qué entrega
`escalation_service.py`: funciones `create_escalamiento()`, `notify_neuroasesor()`, `register_human_response()`, `check_sla_compliance()`, y `handle_sla_breach()`. Gestiona los 7 tipos de escalamiento con sus tiempos objetivo distintos.
