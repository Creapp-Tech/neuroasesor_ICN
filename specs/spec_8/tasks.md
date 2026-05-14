# Tasks — Spec 8: escalation_service.py

- [ ] Implementar `create_escalamiento(paciente: Paciente, tipo: str, motivo: str, fase_origen: str) -> Escalamiento`: crear registro con escalamiento_id (formato ESC-{paciente_id}-{timestamp}), timestamp_escalamiento, tipo, prioridad_paciente copiada del paciente, insertar en tabla escalamientos via db_repository
- [ ] Implementar `notify_neuroasesor(escalamiento: Escalamiento, paciente: Paciente, notas_clinicas: str) -> None`: enviar mensaje WhatsApp al número `config.ICN_NEUROASESOR_WHATSAPP` con datos obligatorios: nombre, teléfono, problema principal, nivel de riesgo, resumen clínico, motivo, prioridad, fase_origen; asignar conversación en ManyChat
- [ ] Implementar `register_human_response(escalamiento_id: str) -> float`: registrar timestamp_respuesta_humano=now(), calcular tiempo_respuesta_humano en minutos, retornar minutos transcurridos
- [ ] Implementar `check_sla_compliance(escalamiento: Escalamiento) -> bool`: calcular cumple_sla_15min según tipo_escalamiento (alarma_critica → 5 min, resto → 15 min); actualizar campo en ESCALAMIENTOS
- [ ] Implementar `handle_sla_breach(escalamiento: Escalamiento, paciente: Paciente) -> None`: registrar cumple_sla_15min=False; alertar coordinador ICN por WhatsApp; marcar conversación como vencida en ManyChat; registrar incidencia en resumen diario
- [ ] Implementar `trigger_alarm_escalamiento(paciente: Paciente, motivo_alarma: str, notas: str) -> Escalamiento`: flujo completo para alarma crítica (tipo=alarma_critica); enviar mensaje de urgencias al paciente; notificar Neuroasesor inmediato
- [ ] Escribir prueba en `tests/test_escalation_service.py`: SLA cumplido (respuesta en 10 min), SLA incumplido (respuesta en 20 min), alarma crítica tiene SLA de 5 min
