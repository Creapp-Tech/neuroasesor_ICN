# Spec 3 — alarm_filter.py: Filtro de Alarmas Pre-IA

## Qué resuelve
Implementa el filtro de palabras y frases de alarma clínica que debe ejecutarse ANTES de cualquier llamada al modelo de IA. Si detecta una alarma, el sistema no llama al LLM: activa flag_alarma, notifica al Neuroasesor y orienta al paciente a urgencias.

## Por qué es necesaria
El documento (Sección 8) define este filtro como obligatorio y no negociable. Es la primera línea de defensa clínica del sistema. Alarmas críticas (convulsión activa, ACV, pensamiento suicida) requieren respuesta humana en menos de 5 minutos. Sin este módulo, el sistema podría llamar al LLM con un mensaje de emergencia y demorar la atención.

## Qué entrega
`alarm_filter.py`: función `check_alarm(mensaje: str) -> tuple[bool, str]` que retorna (es_alarma, motivo_detectado). Lista completa de palabras/frases de alarma extraídas del documento. Función auxiliar para normalizar texto (lowercase, sin tildes) antes de comparar.
