# Spec 11 — audit_log.py: Trazabilidad Completa

## Qué resuelve
Implementa el registro de auditoría transversal del sistema. Registra cada turno de conversación en CONVERSACIONES, versiona los prompts activos, registra tokens usados y errores operativos. Garantiza que todo lo que hace el sistema (NeuroAsistente y Neuroasesor) queda trazado con timestamps Colombia.

## Por qué es necesaria
El documento (Secciones 10, 11, instrucciones obligatorias #11) exige trazabilidad completa de todo lo que hacen el NeuroAsistente y el Neuroasesor. Sin auditoría, no es posible hacer control de calidad, detectar respuestas inadecuadas del sistema ni auditar decisiones clínicas.

## Qué entrega
`audit_log.py`: funciones para registrar cada turno en CONVERSACIONES (incluyendo guia_soporte_turno, version_prompt, tokens, flag_alarma), registrar errores operativos, y exponer función de auditoría de calidad que retorna conversaciones de un paciente.
