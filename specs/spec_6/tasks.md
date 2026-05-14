# Tasks — Spec 6: phase_router.py + prompts/

- [x] Crear directorio `prompts/` con archivo `base_v6.txt`: prompt base del sistema (tríada de tono clínico+humano+comercial, reglas absolutas, lenguaje prohibido, placeholder de datos del paciente)
- [x] Crear `prompts/f0_v6.txt`: clasificar intención (teleorientacion vs admin), mensaje inicial de bienvenida ICN Salud
- [x] Crear `prompts/f1_v6.txt`: consentimiento Ley 1581/2012 (tres puntos), captura de nombre/edad/ciudad/aseguramiento, detección de EPS→ADMIN, máx 2 preguntas por turno
- [x] Crear `prompts/f2_v6.txt`: lista de 10 problemas neurológicos, regla de un problema por teleconsulta, F3 obligatoria antes de agenda o precio
- [x] Crear `prompts/f3_v6.txt`: árbol D1-D6 completo para Cefalea/ICHD-3 como ejemplo, instrucción de adaptar por programa_clinico, cierre anticipado permitido (V5), lenguaje de teleorientación obligatorio
- [x] Crear `prompts/f4_v6.txt`: estructura T1-T4 (resultado clínico, consecuencia, propuesta, cierre), manejo de objeciones, escalamiento comercial al tercer turno sin decisión, cierre con horarios concretos
- [x] Crear `prompts/admin_v6.txt`: redirección a `https://icnsalud.com/#contacto`
- [x] Crear `prompts/humano_v6.txt`: mensaje de espera "un asesor te contactará"
- [x] Implementar `phase_router.py` clase `PhaseRouter` con método `get_system_prompt(fase: str, paciente: Paciente) -> str`: carga el archivo de prompt de la fase, inyecta datos del paciente (nombre, edad, ciudad, aseguramiento, fase_actual, programa_clinico, nivel_riesgo) como variables
- [x] Implementar `get_next_phase(paciente: Paciente, response_ia: ResponseIA, score_result: Optional[dict], error_json: bool) -> str`: lógica de transición backend (no depender del modelo para esta decisión)
- [x] Implementar regla F3 obligatoria: si paciente pide precio/cita en F2, mantener en F2 y redirigir a F3
- [x] Implementar detección de EPS en notas_internas: si tipo=admin → ADMIN
- [x] Implementar detección de escalamiento comercial en F4: si 3+ turnos en F4 sin conversión → registrar requiere_neuroasesor_comercial=True
- [x] Escribir prueba en `tests/test_phase_router.py`: transición F3→F4 (Moderado/Alto), F3→HUMANO (Alarma), F0→ADMIN (EPS)
