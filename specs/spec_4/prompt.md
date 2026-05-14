# Prompt — Spec 4: llm_client.py + json_guard.py

Eres un Ingeniero de Backend Python especializado en integración con LLMs. Tu tarea es implementar el cliente de IA y el guardián de JSON para el sistema NeurOrientador de ICN Salud.

## Contexto
El sistema usa Gemini (V6) como modelo principal. El modelo SIEMPRE debe responder con JSON válido en la estructura `ResponseIA` definida en `schemas.py`. Si el JSON es inválido, el sistema reintenta máximo 2 veces antes de escalar a humano. Los archivos `config.py`, `schemas.py` ya existen.

## Entrega requerida

### Archivo 1: `llm_client.py`
```python
class LLMClient:
    def call(
        self, 
        system_prompt: str, 
        historial: list[dict],  # formato [{role: "user"|"assistant", content: str}]
        mensaje_actual: str
    ) -> tuple[str, int]:
        """
        Llama al modelo de IA.
        Returns: (respuesta_texto_raw, tokens_usados)
        """
```
- Usar `google-generativeai` para Gemini; si `OPENAI_API_KEY` está configurada como alternativa, usar `openai`
- max_tokens = config.MAX_TOKENS (800)
- El historial se formatea correctamente para la API del modelo elegido
- El system_prompt se inyecta como instrucción de sistema

### Archivo 2: `json_guard.py`
```python
def parse_and_validate(raw_text: str) -> Optional[ResponseIA]:
    """Parsea y valida JSON. Retorna None si falla."""

def safe_call_llm(
    client: LLMClient,
    system_prompt: str,
    historial: list,
    mensaje: str
) -> tuple[Optional[ResponseIA], int, bool]:
    """
    Llama al LLM con reintento automático ante JSON inválido.
    
    Flujo:
    1. Llamar con prompt normal → si JSON válido, retornar
    2. Si JSON inválido: agregar al prompt "Responde SOLO JSON válido sin texto adicional ni markdown"
    3. Segundo intento → si válido, retornar
    4. Tercer intento igual → si persiste, retornar (None, tokens_total, True)
    
    Returns: (ResponseIA o None, tokens_totales, error_json_persistente: bool)
    """
```

## Estructura JSON esperada del modelo
El modelo debe responder EXACTAMENTE con:
```json
{
  "respuesta_visible": "texto al paciente",
  "notas_internas": "solo para equipo ICN",
  "puntaje_dominio": {"D1": 0, "D2": 0, "D3": 0, "D4": 0, "D5": 0, "D6": 0},
  "guia_soporte": "ICHD-3 criterio X",
  "cie10": "G43.009"
}
```
NOTA: nivel_riesgo, score_total, flag_alarma y fase_siguiente los calcula el backend Python, NUNCA el modelo.

## Pruebas: `tests/test_json_guard.py`
- JSON válido completo → retorna ResponseIA
- JSON válido sin campos opcionales (guia_soporte, cie10) → retorna ResponseIA
- JSON con texto adicional antes del bloque → debe extraer el JSON si está presente
- String vacío → retorna None
- JSON con campos faltantes obligatorios → retorna None
