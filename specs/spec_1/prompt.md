# Prompt — Spec 1: config.py + schemas.py

Eres un Arquitecto de Software Python especializado en sistemas de salud con IA. Tu tarea es implementar la capa base de configuración y modelos de datos para el agente NeurOrientador de ICN Salud.

## Contexto del sistema
NeurOrientador es un sistema de teleorientación neurológica que opera por WhatsApp + ManyChat, usa Gemini como LLM, y persiste datos en PostgreSQL. La lógica crítica (scoring, alarmas, fases) vive en Python backend, no en prompts de IA. La autoridad de versiones es V6 del documento de contexto.

## Entrega requerida

### Archivo 1: `config.py`
Crea un módulo de configuración que:
- Cargue todas las variables de entorno con `python-dotenv` (nunca hardcodear secretos)
- Variables requeridas: GEMINI_API_KEY, OPENAI_API_KEY, WHATSAPP_TOKEN, WHATSAPP_PHONE_ID, WHATSAPP_WEBHOOK_SECRET, MANYCHAT_API_TOKEN, DATABASE_URL (formato: `postgresql+asyncpg://user:password@host:5432/neurorientador`), ICN_NEUROASESOR_WHATSAPP, ICN_COORDINADOR_WHATSAPP, TZ=America/Bogota
- Constantes del sistema (hardcodeadas, no en .env):
  - MAX_TOKENS = 800
  - MAX_HISTORIAL_TURNOS = 20
  - SCORE_BAJO_MAX = 4
  - SCORE_MODERADO_MAX = 8
  - SCORE_ALTO_MAX = 12
  - SCORE_ALARMA_MIN = 13
  - D1_FLAG_THRESHOLD = 2 (dos o más banderas rojas activan flag_alarma)
  - SLA_MINUTOS = 15
  - SLA_ALARMA_MINUTOS = 5
  - COLOMBIA_TZ = pytz.timezone("America/Bogota")
  - VERSION_FLUJO = "v6.0"

### Archivo 2: `schemas.py`
Crea modelos Pydantic para todas las entidades. Usa `Optional` donde el campo puede estar vacío. Todos los campos deben corresponder exactamente a los definidos en el documento de contexto V6.

**Modelos requeridos:**
1. `Paciente` — todos los campos de la tabla PACIENTES (incluyendo: paciente_id, telefono como clave primaria, nombre, edad, ciudad, aseguramiento, entidad_prepagada, consentimiento_datos_clinicos: bool, consentimiento_teleorientacion: bool, consentimiento_investigacion: bool, timestamp_consentimiento, fase_actual: Literal["F0","F1","F2","F3","F4","ADMIN","HUMANO"], tipo_consulta, programa_clinico, problema_seleccionado, guia_soporte, cie10, nivel_riesgo: Literal["Bajo","Moderado","Alto","Alarma"], score_total: int, fenotipo_probable, respuestas_orientacion, reporte_enviado: bool, conversion, fecha_cita, canal_agenda, estado_cita, fecha_primera_orientacion, fecha_ultima_orientacion, cohorte, requiere_humano: bool, requiere_revision_medica: bool, motivo_escalamiento, error_json: bool, error_operativo, version_prompt, version_flujo, historial_json, notas_internas, fecha_creacion, ultima_actividad, prioridad_operativa: Literal["agendado","particular","general"])

2. `Conversacion` — conv_id, paciente_id, telefono, fase, mensaje_usuario, respuesta_agente, guia_soporte_turno, timestamp, tokens_usados: int, flag_alarma: bool, escalado_humano: bool, version_prompt

3. `Cita` — cita_id, paciente_id, tipo, programa, fecha_cita, hora_cita, canal_agenda, confirmacion, seguimiento_post: bool, resultado_post

4. `Escalamiento` — escalamiento_id, paciente_id, timestamp_escalamiento, timestamp_respuesta_humano (Optional), tiempo_respuesta_humano (Optional float), cumple_sla_15min (Optional bool), tipo_escalamiento: Literal["alarma_critica","clinico","comercial","solicitud_paciente","error_sistema","neuroasistente_clinico","neuroasistente_comercial"], prioridad_paciente: Literal["agendado","particular","general"], fase_origen, motivo, resolucion (Optional), responsable (Optional), resultado (Optional)

5. `NeuroAsistenteInteraccion` — interaccion_id, paciente_id, cita_id (Optional), fecha_hora, canal_contacto, tipo_interaccion: Literal["confirmacion_cita","preparacion_cita","recordatorio","seguimiento_post_cita","resolucion_duda","acompañamiento","oportunidad_comercial"], mensaje_enviado, respuesta_paciente (Optional), estado_interaccion: Literal["enviado","respondido","pendiente","cerrado","escalado"], requiere_revision_clinica: bool, requiere_revision_comercial: bool, notas_internas (Optional), responsable: Literal["NeuroAsistente_automatico","Neuroasesor_humano","Sistema_Make"], accion_generada, prioridad_paciente, version_flujo, timestamp_actualizacion (Optional)

6. `NeuroAsesorInteraccion` — neuroasesor_interaccion_id, paciente_id, fecha_hora_inicio, fecha_hora_fin (Optional), tiempo_respuesta_humano (Optional float), cumple_sla_15min (Optional bool), canal, tipo_interaccion: Literal["escalamiento_clinico","escalamiento_comercial","supervision_neuroasistente","contacto_proactivo","soporte","cierre_comercial"], prioridad_paciente, resumen_conversacion, resultado: Literal["cerrado","pendiente","escalado_medico","nueva_cita_agendada","rechazo","sin_respuesta"], oportunidad_detectada (Optional), incidencia (Optional), notas_internas (Optional), responsable, version_flujo

7. `ResumenDiario` — resumen_id, fecha, total_interacciones_na: int, total_respondidas: int, total_sin_respuesta: int, casos_revision_clinica: int, casos_revision_comercial: int, total_escalamientos: int, sla_cumplido_pct: float, tiempo_respuesta_promedio: float, total_interacciones_neuroasesor: int, resumen_narrativo (Optional), incidencias_sla: int, oportunidades_detectadas: int

8. `ResponseIA` — respuesta_visible: str, notas_internas: str, puntaje_dominio: Dict[str, int] (claves D1 a D6), guia_soporte: Optional[str], cie10: Optional[str]

## Formato de salida esperado
- Dos archivos Python completos: `config.py` y `schemas.py`
- Código limpio, con docstrings breves en clases y funciones
- Sin lógica de negocio en estos archivos (solo configuración y modelos)
- Incluir al final: `requirements.txt` con las dependencias necesarias (pydantic, python-dotenv, pytz, sqlalchemy, asyncpg, alembic, httpx)

## Reglas del sistema (no violar en ningún caso)
- Nunca hardcodear tokens, API keys ni webhooks
- Los campos `nivel_riesgo`, `score_total`, `flag_alarma` y `fase_siguiente` los calcula el backend Python, nunca el modelo de IA
- El campo `historial_json` se almacena como string JSON en Sheets y se deserializa en Python
