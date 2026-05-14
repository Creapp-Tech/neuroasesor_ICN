# Tasks — Spec 9: neuroasistente_service.py

- [ ] Implementar `send_confirmacion_cita(paciente: Paciente, cita: Cita) -> NeuroAsistenteInteraccion`: generar mensaje de confirmación con datos de la cita; enviar por WhatsApp; registrar interaccion con tipo=confirmacion_cita, estado=enviado
- [ ] Implementar `send_preparacion_cita(paciente: Paciente, cita: Cita) -> NeuroAsistenteInteraccion`: generar mensaje de preparación (instrucciones según programa_clinico); registrar tipo=preparacion_cita
- [ ] Implementar `send_recordatorio(paciente: Paciente, cita: Cita) -> NeuroAsistenteInteraccion`: enviar recordatorio 1 día antes; tono cálido, no de notificación automática; registrar tipo=recordatorio
- [ ] Implementar `send_seguimiento_post_cita(paciente: Paciente, cita: Cita) -> NeuroAsistenteInteraccion`: enviar 1 día DESPUÉS de la fecha de cita; preguntar cómo le fue, si entendió todo, si necesita ayuda; registrar tipo=seguimiento_post_cita
- [ ] Implementar `process_patient_response(interaccion_id: str, respuesta: str) -> None`: actualizar respuesta_paciente, estado=respondido; llamar `analyze_response()` para detectar señales; actualizar flags
- [ ] Implementar `analyze_response(respuesta: str, tipo_interaccion: str) -> tuple[bool, bool]`: retorna (requiere_revision_clinica, requiere_revision_comercial); aplicar tabla de señales del documento (complicación post-cita → clínica, cancelación → comercial, interés nuevo programa → comercial)
- [ ] Implementar `handle_no_response(interaccion_id: str, horas_sin_respuesta: int) -> None`: 24h sin respuesta → estado=pendiente; 48h más → estado=cerrado, notas="sin respuesta tras 2 intentos"
- [ ] Implementar `trigger_escalamiento_neuroasistente(interaccion: NeuroAsistenteInteraccion, paciente: Paciente, tipo: str) -> None`: llamar escalation_service con tipo neuroasistente_clinico o neuroasistente_comercial
- [ ] Escribir prueba en `tests/test_neuroasistente_service.py`: respuesta con complicación → clínica=True; cancelación → comercial=True; confirmación normal → ambos False
