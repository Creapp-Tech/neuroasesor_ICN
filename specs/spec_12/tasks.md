# Tasks — Spec 12: tests/ Suite Completa

- [ ] Completar/revisar `tests/test_alarm_filter.py`: mínimo 5 positivos, 5 negativos, variantes con/sin tildes
- [ ] Completar/revisar `tests/test_json_guard.py`: JSON válido, malformado, vacío, campos faltantes
- [ ] Completar/revisar `tests/test_scoring.py`: todos los niveles de riesgo, flag_alarma por D1, edge cases
- [ ] Escribir `tests/test_phase_router.py`: transición F3→F4 (Alto), F3→HUMANO (Alarma), F0→ADMIN (EPS), F4 con 3 turnos sin conversión → HUMANO
- [ ] Escribir `tests/test_escalation_sla.py`: SLA cumplido, SLA vencido (cumple_sla_15min=False → handle_sla_breach llamado), alarma_critica con SLA 5 min
- [ ] Escribir `tests/test_flujo_eps_admin.py`: paciente que menciona EPS → fase=ADMIN, link icnsalud.com enviado, no pasa a F1 clínico
- [ ] Escribir `tests/test_solicitud_humano.py`: paciente pide hablar con persona → fase=HUMANO, notify_neuroasesor llamado
- [ ] Escribir `tests/test_flujo_completo.py`: integración del flujo principal con mocks (webhook → alarm_filter OK → call LLM → score → F3→F4 → registrar en PostgreSQL)
- [ ] Crear `conftest.py` con fixtures compartidos: paciente_test, cita_test, escalamiento_test, mock_db_repo
- [ ] Verificar que `pytest` corre todos los tests sin errores: `pytest tests/ -v`
