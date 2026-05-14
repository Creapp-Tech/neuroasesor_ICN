# Spec 12 — tests/: Suite de Pruebas Unitarias Obligatorias

## Qué resuelve
Implementa la suite completa de pruebas unitarias requeridas por el documento para validar los módulos críticos del sistema: alarmas, JSON inválido, scoring, transición F3→F4, solicitud de humano, paciente EPS/admin y SLA vencido.

## Por qué es necesaria
El documento (Sección 20, criterio de aceptación) lista explícitamente las pruebas requeridas: "Tiene pruebas unitarias para: alarmas, JSON inválido, scoring, transición F3→F4, solicitud de humano, paciente EPS/admin, SLA vencido." Sin estas pruebas, la implementación no cumple los criterios de aceptación del proyecto.

## Qué entrega
`tests/` con archivos de prueba para cada módulo crítico. Incluye pruebas de integración básica del flujo principal (webhook → alarm_filter → llm_client → scoring → phase_router → db_repository). Usa `pytest` con `unittest.mock` para mockear llamadas externas (PostgreSQL, WhatsApp, LLM).
