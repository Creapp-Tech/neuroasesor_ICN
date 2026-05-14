import json
import re
from typing import Optional, Tuple

from pydantic import ValidationError

from app.schemas import ResponseIA
from app.llm_client import LLMClient


def parse_and_validate(raw_text: str) -> Optional[ResponseIA]:
    """
    Extract and validate a ResponseIA JSON from raw LLM output.

    Tries direct parse first; if that fails, uses a regex to pull the first
    {...} block from the text (handles markdown fences and surrounding prose).
    Returns None on any parse or validation error.
    """
    if not raw_text:
        return None

    try:
        match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        json_str = match.group(0) if match else raw_text
        data = json.loads(json_str)
        return ResponseIA(**data)
    except (json.JSONDecodeError, ValidationError, ValueError, AttributeError):
        return None


def safe_call_llm(
    client: LLMClient,
    system_prompt: str,
    historial: list,
    mensaje: str,
) -> Tuple[Optional[ResponseIA], int, bool]:
    """
    Call the LLM with up to 3 attempts, tightening the JSON instruction on failure.

    Returns:
        (ResponseIA | None, total_tokens_used, error_json_persistente)
    """
    total_tokens = 0
    current_prompt = system_prompt

    for attempt in range(1, 4):
        try:
            raw_response, tokens = client.call(current_prompt, historial, mensaje)
            total_tokens += tokens

            result = parse_and_validate(raw_response)
            if result:
                return result, total_tokens, False

            if attempt == 1:
                current_prompt += (
                    "\n\nIMPORTANTE: Responde EXCLUSIVAMENTE con un objeto JSON válido. "
                    "Sin explicaciones, sin bloques markdown (```json). Solo el JSON."
                )
        except Exception:
            pass

    return None, total_tokens, True
