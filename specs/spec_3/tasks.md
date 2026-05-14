# Tasks — Spec 3: alarm_filter.py

- [x] Definir lista `ALARM_KEYWORDS` con todas las frases del documento Sección 8: "convulsión", "convulsiones", "pérdida de conciencia", "desmayo", "no puedo mover brazo", "no puedo mover pierna", "no puedo mover cara", "peor dolor de mi vida", "dolor de inicio súbito", "rigidez de nuca", "fiebre + cuello", "pensamiento suicida", "hacerme daño", "cefalea en trueno", "visión doble súbita", "no puedo hablar de repente", "convulsión activa", "acv probable"
- [x] Implementar función `normalize_text(text: str) -> str`: convertir a minúsculas, eliminar tildes y caracteres especiales, para comparación robusta
- [x] Implementar función `check_alarm(mensaje: str) -> tuple[bool, str]`: normalizar el mensaje, buscar cada keyword; retornar (True, keyword_detectada) si hay match, (False, "") si no
- [x] Escribir prueba unitaria básica en `tests/test_alarm_filter.py` que verifica: mensajes con alarma retornan True, mensajes normales retornan False
