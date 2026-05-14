# Tasks — Spec 5: scoring.py

- [x] Implementar `should_flag_alarm(puntaje_dominio: dict) -> bool`: retorna True si D1 >= config.D1_FLAG_THRESHOLD (2)
- [x] Implementar `calculate_score(puntaje_dominio: dict) -> int`: suma valores D1+D2+D3+D4+D5+D6; manejar claves faltantes como 0
- [x] Implementar `classify_risk(score: int, flag_alarma: bool) -> Literal["Bajo","Moderado","Alto","Alarma"]`: Alarma si flag_alarma=True o score>=13; Alto si 9-12; Moderado si 5-8; Bajo si 0-4
- [x] Implementar `get_fase_siguiente_f3(nivel_riesgo: str) -> Literal["F4","HUMANO"]`: Alto/Moderado → "F4"; Alarma → "HUMANO"; Bajo → "F4" (en MVP V6, F6 está pospuesto)
- [x] Implementar función integradora `process_f3_scoring(puntaje_dominio: dict) -> dict`: retorna dict con score_total, nivel_riesgo, flag_alarma, fase_siguiente
- [x] Escribir pruebas unitarias en `tests/test_scoring.py`: score 13+ → Alarma; D1=2 → flag_alarma True; score 9-12 → Alto→F4; score 5-8 → Moderado→F4; score 0-4 → Bajo
