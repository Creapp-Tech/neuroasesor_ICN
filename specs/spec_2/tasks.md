# Tasks — Spec 2: db_repository.py + models.py

- [x] Crear `migrations/001_initial_schema.sql` con todos los ENUMs y tablas (pacientes, conversaciones, citas, etc.) según esquema V6.
- [x] Definir tablas en Supabase con sus claves primarias, FKs e índices optimizados.
- [x] Implementar `SupabaseRepository` en `app/supabase_repository.py` con cliente oficial `supabase-py`.
- [x] Implementar `get_paciente_by_telefono(telefono: str) -> Optional[Paciente]`.
- [x] Implementar `create_paciente(paciente: Paciente) -> Paciente`.
- [x] Implementar `update_paciente(telefono: str, campos: dict) -> None`.
- [x] Implementar `insert_conversacion(conv: Conversacion) -> None`.
- [x] Implementar `insert_cita(cita: Cita) -> None` y `update_cita(cita_id: str, campos: dict) -> None`.
- [x] Implementar `get_citas_pendientes_seguimiento() -> List[Cita]`.
- [x] Implementar `insert_escalamiento(esc: Escalamiento) -> None` y `update_escalamiento(escalamiento_id: str, campos: dict) -> None`.
- [x] Implementar `get_escalamientos_sin_respuesta() -> List[Escalamiento]`.
- [x] Implementar `insert_neuroasistente_interaccion`, `update_neuroasistente_interaccion`, `get_interacciones_del_dia(fecha)`, `get_interaccion_activa_por_paciente`.
- [x] Implementar `insert_neuroasesor_interaccion`, `insert_resumen_diario`.
- [x] Implementar `insert_cohorte_investigacion(paciente: Paciente)` con anonimización y verificación de consentimiento.
- [x] Agregar manejo de errores con retry y capturar `postgrest.exceptions.APIError`.
- [x] Actualizar `requirements.txt` con `supabase>=2.0.0`.

