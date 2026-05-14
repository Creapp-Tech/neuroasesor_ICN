# Tasks — Spec 11: audit_log.py

- [ ] Implementar `log_turno(paciente_id, telefono, fase, mensaje_usuario, respuesta_agente, guia_soporte_turno, tokens_usados, flag_alarma, version_prompt) -> Conversacion`: crear conv_id (formato CONV-{paciente_id}-{timestamp}), insertar en CONVERSACIONES, retornar objeto Conversacion
- [ ] Implementar `log_error_operativo(paciente_id: str, descripcion: str, tipo: str) -> None`: registrar error en notas del paciente; logging Python con nivel ERROR
- [ ] Implementar `update_historial(paciente: Paciente, mensaje_usuario: str, respuesta_agente: str) -> list`: agregar turno al historial_json del paciente; si len > config.MAX_HISTORIAL_TURNOS, eliminar el más antiguo; retornar historial actualizado
- [ ] Implementar `get_conversaciones_paciente(paciente_id: str) -> List[Conversacion]`: leer historial de CONVERSACIONES para auditoría de calidad
