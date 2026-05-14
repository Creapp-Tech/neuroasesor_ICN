# Spec 4 — llm_client.py + json_guard.py: Cliente LLM y Validación JSON

## Qué resuelve
Encapsula todas las llamadas al modelo de IA (Gemini o OpenAI) y la validación estricta de la respuesta JSON. Implementa el mecanismo de reintentos automáticos ante JSON inválido (máximo 2 reintentos) y el escalamiento a HUMANO si el JSON persiste inválido al tercer fallo.

## Por qué es necesaria
El documento (Secciones 9, 10) exige que toda salida del modelo sea JSON válido en la estructura establecida. El sistema debe reintentar con instrucción "Responde SOLO JSON válido" antes de escalar. Sin esta capa, un JSON inválido del LLM rompe el flujo completo del paciente.

## Qué entrega
- `llm_client.py`: cliente Gemini/OpenAI que recibe system_prompt + historial + mensaje_actual y retorna `ResponseIA`. Registra tokens usados.
- `json_guard.py`: parsea, valida y reintenta JSON. Si falla 3 veces, retorna señal de escalamiento a HUMANO y registra `error_json=True`.
