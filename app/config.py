"""Configuration module for NeurOrientador.

Loads required environment variables using `python-dotenv` and defines
system-wide constants. No secrets are hard-coded; they are read from the
environment at runtime.
"""

import os
from pathlib import Path
from typing import Final

import pytz
from dotenv import load_dotenv

# Load .env file located at the project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

def _get_env(name: str, default: str = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise EnvironmentError(f"Required environment variable '{name}' is not set")
    return value

# --- Required Secrets and Environment Variables ---
GEMINI_API_KEY: Final[str] = _get_env("GEMINI_API_KEY", "placeholder")
OPENAI_API_KEY: Final[str] = _get_env("OPENAI_API_KEY", "placeholder")

# --- Optional LLM providers (set one to use it) ---
ANTHROPIC_API_KEY: Final[str] = _get_env("ANTHROPIC_API_KEY", "placeholder")
OPENROUTER_API_KEY: Final[str] = _get_env("OPENROUTER_API_KEY", "placeholder")
OPENROUTER_MODEL: Final[str] = _get_env("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")
WHATSAPP_TOKEN: Final[str] = _get_env("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID: Final[str] = _get_env("WHATSAPP_PHONE_ID")
WHATSAPP_WEBHOOK_SECRET: Final[str] = _get_env("WHATSAPP_WEBHOOK_SECRET")
MANYCHAT_API_TOKEN: Final[str] = _get_env("MANYCHAT_API_TOKEN")
DATABASE_URL: Final[str] = _get_env("DATABASE_URL")  # Format: postgresql+asyncpg://user:password@host:5432/neurorientador
SUPABASE_URL: Final[str] = _get_env("SUPABASE_URL")
SUPABASE_SERVICE_KEY: Final[str] = _get_env("SUPABASE_SERVICE_KEY")
ICN_NEUROASESOR_WHATSAPP: Final[str] = _get_env("ICN_NEUROASESOR_WHATSAPP")
ICN_COORDINADOR_WHATSAPP: Final[str] = _get_env("ICN_COORDINADOR_WHATSAPP")
TZ: Final[str] = _get_env("TZ", "America/Bogota")

# --- Twilio WhatsApp (alternative to Meta Cloud API) ---
TWILIO_ACCOUNT_SID: Final[str] = _get_env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN: Final[str] = _get_env("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM: Final[str] = _get_env("TWILIO_WHATSAPP_FROM")

# --- System Constants (Hard-coded) ---
MAX_TOKENS: Final[int] = 800
MAX_HISTORIAL_TURNOS: Final[int] = 20
SCORE_BAJO_MAX: Final[int] = 4
SCORE_MODERADO_MAX: Final[int] = 8
SCORE_ALTO_MAX: Final[int] = 12
SCORE_ALARMA_MIN: Final[int] = 13
D1_FLAG_THRESHOLD: Final[int] = 2  # Two or more red flags activate flag_alarma
SLA_MINUTOS: Final[int] = 15
SLA_ALARMA_MINUTOS: Final[int] = 5
COLOMBIA_TZ = pytz.timezone("America/Bogota")
VERSION_FLUJO: Final[str] = "v6.0"
