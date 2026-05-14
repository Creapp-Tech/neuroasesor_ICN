# Spec 5 — scoring.py: Cálculo de Score, Nivel de Riesgo y Flag de Alarma

## Qué resuelve
Implementa la lógica de scoring del árbol clínico F3: suma los puntajes D1-D6 entregados por el modelo IA, calcula el `score_total`, clasifica el `nivel_riesgo` (Bajo/Moderado/Alto/Alarma) y activa `flag_alarma`. Esta lógica vive en Python backend, nunca en el prompt del modelo.

## Por qué es necesaria
El documento (Secciones 3.1, 9, 10) es explícito: la lógica de scoring NO debe residir en prompts de IA. Make/backend calcula score_total y nivel_riesgo. Los umbrales son fijos: 0-4 Bajo, 5-8 Moderado, 9-12 Alto, ≥13 o flag_alarma Alarma. D1 ≥ 2 activa flag_alarma inmediato.

## Qué entrega
`scoring.py`: funciones `calculate_score(puntaje_dominio: dict) -> int`, `classify_risk(score: int, flag_alarma: bool) -> str`, `should_flag_alarm(puntaje_dominio: dict) -> bool`, y `get_fase_siguiente(nivel_riesgo: str) -> str` con la tabla de transición F3→F4/HUMANO.
