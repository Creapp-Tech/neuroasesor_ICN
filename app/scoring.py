from typing import Dict, Literal
from app import config


def should_flag_alarm(puntaje_dominio: Dict[str, int]) -> bool:
    """Return True if D1 (Red Flags) >= D1_FLAG_THRESHOLD (default 2)."""
    return puntaje_dominio.get("D1", 0) >= config.D1_FLAG_THRESHOLD


def calculate_score(puntaje_dominio: Dict[str, int]) -> int:
    """Sum D1 through D6. Missing keys count as 0."""
    return sum(puntaje_dominio.get(f"D{i}", 0) for i in range(1, 7))


def classify_risk(score: int, flag_alarma: bool) -> Literal["Bajo", "Moderado", "Alto", "Alarma"]:
    """
    0-4   → Bajo
    5-8   → Moderado
    9-12  → Alto
    >=13 or flag_alarma → Alarma
    """
    if flag_alarma or score >= config.SCORE_ALARMA_MIN:
        return "Alarma"
    if score >= 9:
        return "Alto"
    if score >= 5:
        return "Moderado"
    return "Bajo"


def get_fase_siguiente_f3(nivel_riesgo: str) -> Literal["F4", "HUMANO"]:
    """Alarma → HUMANO; everything else → F4 (conversion)."""
    return "HUMANO" if nivel_riesgo == "Alarma" else "F4"


def process_f3_scoring(puntaje_dominio: Dict[str, int]) -> dict:
    """Integrate all F3 scoring logic into a single result dict."""
    flag_alarma = should_flag_alarm(puntaje_dominio)
    score_total = calculate_score(puntaje_dominio)
    nivel_riesgo = classify_risk(score_total, flag_alarma)
    fase_siguiente = get_fase_siguiente_f3(nivel_riesgo)

    return {
        "score_total": score_total,
        "nivel_riesgo": nivel_riesgo,
        "flag_alarma": flag_alarma,
        "fase_siguiente": fase_siguiente,
    }
