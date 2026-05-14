# Prompt — Spec 3: alarm_filter.py

Eres un Ingeniero de Software Python especializado en sistemas de salud. Tu tarea es implementar el filtro de alarmas clínicas del sistema NeurOrientador de ICN Salud.

## Contexto
Este filtro se ejecuta ANTES de llamar al LLM en cada mensaje entrante. Si detecta una alarma clínica, el sistema NO llama al modelo de IA. Es la primera línea de seguridad clínica del sistema. Los `config.py` y `schemas.py` ya existen.

## Entrega requerida: `alarm_filter.py`

### Lista de alarmas (extraída literalmente del documento V6/V5)
Estas son las palabras y frases que activan la alarma. Normaliza el texto antes de comparar (lowercase, sin tildes):

```
convulsion / convulsiones
perdida de conciencia / desmayo
no puedo mover (brazo/pierna/cara)
peor dolor de mi vida / de inicio subito
rigidez de nuca / fiebre + cuello
pensamiento suicida / hacerme daño
cefalea en trueno
vision doble subita
no puedo hablar de repente
convulsion activa
acv probable
```

### Funciones requeridas

```python
def normalize_text(text: str) -> str:
    """Convierte a lowercase y elimina tildes para comparación robusta."""

def check_alarm(mensaje: str) -> tuple[bool, str]:
    """
    Verifica si el mensaje contiene palabras/frases de alarma clínica.
    
    Returns:
        (True, keyword_detectada) si hay alarma
        (False, "") si no hay alarma
    
    IMPORTANTE: No llamar al LLM si retorna True.
    """
```

### Comportamiento esperado
- "me está dando una convulsión" → (True, "convulsion")
- "tengo el peor dolor de mi vida" → (True, "peor dolor de mi vida")
- "me duele la cabeza hace 3 días" → (False, "")
- "pensé en hacerme daño anoche" → (True, "hacerme daño")

## Archivo de pruebas: `tests/test_alarm_filter.py`
Crea pruebas unitarias con `pytest` que validen al menos:
- 5 casos positivos (mensajes con alarma)
- 5 casos negativos (mensajes normales sin alarma)
- Variantes con tildes y sin tildes para el mismo caso

## Formato de salida
Dos archivos: `alarm_filter.py` y `tests/test_alarm_filter.py`
