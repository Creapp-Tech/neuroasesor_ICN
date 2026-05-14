import unicodedata
import re
from typing import Tuple, Optional


ALARM_KEYWORDS = [
    "convulsion",
    "convulsiones",
    "perdida de conciencia",
    "desmayo",
    "no puedo mover brazo",
    "no puedo mover pierna",
    "no puedo mover cara",
    "no puedo mover",
    "peor dolor de mi vida",
    "dolor de inicio subito",
    "de inicio subito",
    "rigidez de nuca",
    "fiebre + cuello",
    "pensamiento suicida",
    "hacerme dano",
    "cefalea en trueno",
    "vision doble subita",
    "no puedo hablar de repente",
    "convulsion activa",
    "acv probable",
]


def normalize_text(text: Optional[str]) -> str:
    """Lowercase + remove accents. Preserves spaces, digits and '+' for compound keywords."""
    if not text:
        return ""
    # Strip accents
    text = "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )
    text = text.lower().strip()
    # Keep only letters, digits, spaces and '+'
    text = re.sub(r"[^a-z0-9\s\+]", "", text)
    return text


def check_alarm(mensaje: Optional[str]) -> Tuple[bool, str]:
    """Return (True, keyword) if the message contains a clinical alarm keyword, else (False, '')."""
    if not mensaje:
        return False, ""

    normalized = normalize_text(mensaje)
    for keyword in ALARM_KEYWORDS:
        if keyword in normalized:
            return True, keyword

    return False, ""
