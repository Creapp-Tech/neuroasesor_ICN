# Prompt — Spec 5: scoring.py

Eres un Ingeniero de Backend Python con experiencia en sistemas clínicos. Tu tarea es implementar el motor de scoring del árbol clínico F3 para el sistema NeurOrientador de ICN Salud.

## Contexto
Esta lógica es crítica y NO puede residir en prompts de IA. El modelo de IA solo reporta `puntaje_dominio` (valores D1-D6). Python calcula todo lo demás. Los umbrales están definidos en `config.py` (ya implementado).

## Reglas de scoring (del documento V6/V5)
- D1 (Banderas rojas): 0=ninguna, 1=una bandera, 3=dos o más → si D1 >= 2: flag_alarma = True
- Score total = suma D1+D2+D3+D4+D5+D6 (máximo teórico: 15 para Cefalea)
- Clasificación:
  - 0-4: Bajo
  - 5-8: Moderado → F4
  - 9-12: Alto → F4
  - ≥13 o flag_alarma=True: Alarma → HUMANO

## Entrega requerida: `scoring.py`

```python
def should_flag_alarm(puntaje_dominio: dict) -> bool:
    """D1 >= 2 activa flag de alarma inmediato."""

def calculate_score(puntaje_dominio: dict) -> int:
    """Suma D1+D2+D3+D4+D5+D6. Claves faltantes = 0."""

def classify_risk(score: int, flag_alarma: bool) -> str:
    """Retorna: "Bajo", "Moderado", "Alto" o "Alarma"."""

def get_fase_siguiente_f3(nivel_riesgo: str) -> str:
    """
    Retorna fase siguiente al completar F3.
    Alto/Moderado/Bajo → "F4"
    Alarma → "HUMANO"
    Nota: En MVP V6, F6 está pospuesto. Bajo riesgo va a F4 también
    para no dejar al paciente sin conversión.
    """

def process_f3_scoring(puntaje_dominio: dict) -> dict:
    """
    Función integradora. Retorna:
    {
        "score_total": int,
        "nivel_riesgo": str,
        "flag_alarma": bool,
        "fase_siguiente": str
    }
    """
```

## Pruebas: `tests/test_scoring.py`
Casos obligatorios:
- D1=3, score total=14 → Alarma, HUMANO
- D1=2, score total=8 → Alarma (por D1), HUMANO
- D1=0, score total=10 → Alto, F4
- D1=0, score total=6 → Moderado, F4
- D1=0, score total=3 → Bajo, F4
- puntaje_dominio vacío → score=0, Bajo
