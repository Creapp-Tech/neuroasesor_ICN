# Tasks — Spec 10: neuroasesor_service.py + daily_reports.py

- [ ] Implementar `neuroasesor_service.py` función `register_intervencion(paciente_id, tipo, canal, resumen, resultado, responsable, **kwargs) -> NeuroAsesorInteraccion`: crear registro con neuroasesor_interaccion_id (formato NA_H-{paciente_id}-{timestamp}), insertar en NEUROASESOR_INTERACCIONES
- [ ] Implementar `record_escalamiento_atendido(escalamiento_id: str, neuroasesor_nombre: str) -> None`: llamar escalation_service.register_human_response() y crear intervención tipo=escalamiento_clinico o escalamiento_comercial
- [ ] Implementar `daily_reports.py` función `generate_daily_summary() -> ResumenDiario`: filtrar NEUROASISTENTE_INTERACCIONES del día actual; calcular métricas (total, respondidas, sin respuesta, clínicas, comerciales, escalamientos, % SLA, tiempo promedio)
- [ ] Implementar llamada al LLM para generar resumen narrativo del día: prompt "Genera un resumen ejecutivo del día del NeuroAsistente con estos datos. Tono: operativo, claro, directo. Incluye alertas si hay casos clínicos o comerciales pendientes."
- [ ] Implementar `send_daily_summary(resumen: ResumenDiario) -> None`: formatear mensaje según plantilla del documento V6 Documento 5, enviar por WhatsApp al Neuroasesor; insertar ResumenDiario en RESUMENES_DIARIOS
- [ ] Configurar trigger del resumen diario: función `schedule_daily_summary()` que debe ejecutarse a las 8:00 PM Colombia, lunes a sábado (usando APScheduler o similar)
