# Tasks — Spec 4: llm_client.py + json_guard.py

- [x] Implementar `llm_client.py` con clase `LLMClient` que inicializa el cliente Gemini (usando `google-generativeai`) con `config.GEMINI_API_KEY`; incluir fallback a OpenAI si se configura `OPENAI_API_KEY`
- [x] Implementar método `call(system_prompt: str, historial: list, mensaje_actual: str) -> tuple[str, int]`: llama al modelo con max_tokens=config.MAX_TOKENS; retorna (respuesta_raw_text, tokens_usados)
- [x] Implementar `json_guard.py` con función `parse_and_validate(raw_text: str) -> Optional[ResponseIA]`: parsea el JSON, valida estructura contra modelo `ResponseIA`, retorna None si falla
- [x] Implementar función `safe_call_llm(client: LLMClient, system_prompt: str, historial: list, mensaje: str) -> tuple[Optional[ResponseIA], int, bool]` en `json_guard.py`: intento 1 → si falla JSON, intento 2 con prompt "Responde SOLO JSON válido sin texto adicional" → si falla, intento 3 igual → si falla los 3, retorna (None, 0, True) donde True indica error_json persistente
- [x] Asegurar que tokens_usados se acumula correctamente en todos los reintentos y se retorna el total
- [x] Escribir prueba unitaria en `tests/test_json_guard.py`: JSON válido pasa, JSON malformado falla, string vacío falla, JSON con campos faltantes falla
