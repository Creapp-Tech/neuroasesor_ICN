# Spec 1 — config.py + schemas.py: Configuración Base y Modelos de Datos

## Qué resuelve
Establece la capa de configuración centralizada y los modelos Pydantic que toda la aplicación usará como contratos de datos. Sin esta spec, ningún módulo posterior puede funcionar de forma tipada y validada.

## Por qué es necesaria
El documento (Sección 10) lista explícitamente los módulos Python requeridos. `config.py` debe manejar variables de entorno, modelos de IA, tokens, URLs y timezone Colombia. `schemas.py` debe definir los modelos Pydantic para las entidades del sistema: Paciente, Conversacion, Cita, Escalamiento, NeuroAsistenteInteraccion, NeuroAsesorInteraccion, ResumenDiario y la estructura JSON de respuesta del modelo de IA.

## Qué entrega
- `config.py`: carga y expone todas las variables de entorno requeridas (Gemini/OpenAI key, WhatsApp token + phone_id + webhook_secret, ManyChat token, DATABASE_URL PostgreSQL, números internos ICN, timezone Colombia UTC-5). Expone constantes: MAX_TOKENS=800, MAX_HISTORIAL_TURNOS=20, umbrales de scoring (score_alto=9, score_alarma=13, d1_flag=2).
- `schemas.py`: modelos Pydantic con todos los campos de las tablas PACIENTES, CONVERSACIONES, CITAS, ESCALAMIENTOS, NEUROASISTENTE_INTERACCIONES, NEUROASESOR_INTERACCIONES y RESUMENES_DIARIOS definidos en V6. Incluye el modelo `ResponseIA` con campos: respuesta_visible, notas_internas, puntaje_dominio (D1-D6), guia_soporte, cie10.
