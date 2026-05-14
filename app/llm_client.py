"""LLM client with multi-provider support.

Priority order (first configured key wins):
  1. Anthropic Claude   — ANTHROPIC_API_KEY
  2. OpenRouter         — OPENROUTER_API_KEY  (free models available)
  3. OpenAI             — OPENAI_API_KEY
  4. Google Gemini      — GEMINI_API_KEY

Set the desired key in .env; leave the rest as "placeholder".
"""

import anthropic
import google.generativeai as genai
from openai import OpenAI

from app import config

def _active(key: str) -> bool:
    """Return True if key is non-empty and not the literal string 'placeholder'."""
    return bool(key) and key.strip() not in ("", "placeholder")


class LLMClient:
    """Dispatch LLM calls to the first configured provider. Returns (text, tokens)."""

    def __init__(self):
        # Anthropic Claude
        if _active(config.ANTHROPIC_API_KEY):
            self._provider = "claude"
            self._anthropic = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
            return

        # OpenRouter (OpenAI-compatible, free models available)
        if _active(config.OPENROUTER_API_KEY):
            self._provider = "openrouter"
            self._openrouter = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=config.OPENROUTER_API_KEY,
            )
            return

        # OpenAI
        if _active(config.OPENAI_API_KEY):
            self._provider = "openai"
            self._openai = OpenAI(api_key=config.OPENAI_API_KEY)
            return

        # Google Gemini
        if _active(config.GEMINI_API_KEY):
            self._provider = "gemini"
            genai.configure(api_key=config.GEMINI_API_KEY)
            return

        raise ValueError(
            "No LLM provider configured. Set one of: ANTHROPIC_API_KEY, "
            "OPENROUTER_API_KEY, OPENAI_API_KEY, or GEMINI_API_KEY in .env"
        )

    def call(
        self,
        system_prompt: str,
        historial: list[dict],
        mensaje_actual: str,
    ) -> tuple[str, int]:
        """Return (raw_response_text, tokens_used)."""
        if self._provider == "claude":
            return self._call_claude(system_prompt, historial, mensaje_actual)
        if self._provider == "openrouter":
            return self._call_openrouter(system_prompt, historial, mensaje_actual)
        if self._provider == "openai":
            return self._call_openai(system_prompt, historial, mensaje_actual)
        if self._provider == "gemini":
            return self._call_gemini(system_prompt, historial, mensaje_actual)
        raise ValueError(f"Unknown provider: {self._provider}")

    # ── Anthropic Claude ──────────────────────────────────────────────────────

    def _call_claude(
        self, system_prompt: str, historial: list[dict], mensaje_actual: str
    ) -> tuple[str, int]:
        messages = []
        for turn in historial:
            messages.append({"role": turn["role"], "content": turn["content"]})
        messages.append({"role": "user", "content": mensaje_actual})

        response = self._anthropic.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=config.MAX_TOKENS,
            system=system_prompt,
            messages=messages,
        )
        text = response.content[0].text
        tokens = response.usage.input_tokens + response.usage.output_tokens
        return text, tokens

    # ── OpenRouter ────────────────────────────────────────────────────────────

    def _call_openrouter(
        self, system_prompt: str, historial: list[dict], mensaje_actual: str
    ) -> tuple[str, int]:
        messages = [{"role": "system", "content": system_prompt}]
        for turn in historial:
            messages.append({"role": turn["role"], "content": turn["content"]})
        messages.append({"role": "user", "content": mensaje_actual})

        response = self._openrouter.chat.completions.create(
            model=config.OPENROUTER_MODEL,
            messages=messages,
            max_tokens=config.MAX_TOKENS,
            temperature=0.2,
        )
        text = response.choices[0].message.content or ""
        tokens = response.usage.total_tokens if response.usage else 0
        return text, tokens

    # ── OpenAI ────────────────────────────────────────────────────────────────

    def _call_openai(
        self, system_prompt: str, historial: list[dict], mensaje_actual: str
    ) -> tuple[str, int]:
        messages = [{"role": "system", "content": system_prompt}]
        for turn in historial:
            messages.append({"role": turn["role"], "content": turn["content"]})
        messages.append({"role": "user", "content": mensaje_actual})

        response = self._openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=config.MAX_TOKENS,
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content, response.usage.total_tokens

    # ── Google Gemini ─────────────────────────────────────────────────────────

    def _call_gemini(
        self, system_prompt: str, historial: list[dict], mensaje_actual: str
    ) -> tuple[str, int]:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=system_prompt,
        )
        contents = []
        for turn in historial:
            role = "user" if turn["role"] == "user" else "model"
            contents.append({"role": role, "parts": [turn["content"]]})
        contents.append({"role": "user", "parts": [mensaje_actual]})

        response = model.generate_content(
            contents,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=config.MAX_TOKENS,
                temperature=0.2,
            ),
        )
        tokens = (
            response.usage_metadata.total_token_count
            if hasattr(response, "usage_metadata")
            else 0
        )
        return response.text, tokens
