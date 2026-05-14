# Spec 9 — neuroasistente_service.py: Servicio de Acompañamiento Post-Agenda

## Qué resuelve
Implementa el flujo de acompañamiento del NeuroAsistente para pacientes con cita agendada: confirmación de cita, preparación, recordatorio (1 día antes) y seguimiento post-consulta (1 día después). Registra cada interacción en NEUROASISTENTE_INTERACCIONES y aplica la lógica de escalamiento ante señales clínicas o comerciales.

## Por qué es necesaria
El documento (Secciones 15, 22-26, V5 Documentos 6-7) define el NeuroAsistente como componente formal de acompañamiento. El seguimiento es exactamente 1 día después de la cita (V5). Cada interacción debe quedar registrada. Sin respuesta en 24h → pendiente. Sin respuesta en 48h más → cerrado. El NeuroAsistente NO es autónomo: requiere supervisión diaria del Neuroasesor.

## Qué entrega
`neuroasistente_service.py`: funciones para cada tipo de interacción (confirmacion_cita, preparacion_cita, recordatorio, seguimiento_post_cita), análisis de respuesta del paciente para detectar señales clínicas/comerciales, y gestión de estados (enviado→respondido→pendiente→cerrado).
