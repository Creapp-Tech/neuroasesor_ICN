# Prompt — Spec 9: neuroasistente_service.py

Eres un Ingeniero de Backend Python con experiencia en sistemas de salud y acompañamiento al paciente. Tu tarea es implementar el servicio de acompañamiento NeuroAsistente para ICN Salud.

## Contexto
El NeuroAsistente se activa cuando un paciente agenda una cita. Acompaña desde la confirmación hasta 1 día después de la consulta. NO es autónomo: toda interacción se registra para supervisión diaria del Neuroasesor. El tono es cálido y cercano, no de notificación automática. Los specs anteriores ya están implementados.

## Flujo de acompañamiento (del documento V5/V6)
1. Confirmación de cita (inmediata al agendar)
2. Preparación de cita (instrucciones según programa)
3. Recordatorio (1 día antes)
4. Seguimiento post-consulta (1 día DESPUÉS de la fecha de cita)

## Tabla de señales en respuesta del paciente
```
Complicación clínica post-consulta → requiere_revision_clinica=True
Duda sobre medicamento recetado     → requiere_revision_clinica=True
Señal emocional o angustia          → requiere_revision_clinica=True
Inconformidad con el servicio       → requiere_revision_comercial=True
Interés en nuevo programa/reconsulta → requiere_revision_comercial=True
Cancelación sin reagendar           → requiere_revision_comercial=True
Respuesta normal/confirmación       → ambos False
```

## Entrega requerida: `neuroasistente_service.py`

Para cada función de envío:
- Generar el mensaje con el LLM (para mensajes personalizados como seguimiento post-cita) O usar plantilla fija (para recordatorios estándar)
- Enviar por WhatsApp usando `whatsapp_client.send_message()`
- Crear e insertar `NeuroAsistenteInteraccion` con estado=enviado
- Usar `interaccion_id = f"NA-{paciente.paciente_id}-{timestamp_iso}"`

```python
def send_confirmacion_cita(paciente: Paciente, cita: Cita) -> NeuroAsistenteInteraccion
def send_preparacion_cita(paciente: Paciente, cita: Cita) -> NeuroAsistenteInteraccion  
def send_recordatorio(paciente: Paciente, cita: Cita) -> NeuroAsistenteInteraccion
def send_seguimiento_post_cita(paciente: Paciente, cita: Cita) -> NeuroAsistenteInteraccion

def process_patient_response(interaccion_id: str, respuesta: str) -> None:
    """Actualiza respuesta, analiza señales, actualiza flags, escala si aplica."""

def analyze_response(respuesta: str, tipo_interaccion: str) -> tuple[bool, bool]:
    """Returns (requiere_revision_clinica, requiere_revision_comercial)."""

def handle_no_response(interaccion_id: str, horas_sin_respuesta: int) -> None:
    """24h → pendiente. 72h (24+48) → cerrado."""
```

## Mensajes de referencia (del documento V5 - Sección 15.5)
- Seguimiento post-cita: "Hola [nombre] 👋 ¿Cómo te fue ayer en tu consulta con el neurólogo? Queremos saber cómo estás y si quedaste con alguna duda..."
- Tono general: cercano, no de notificación automática, siempre incluir disponibilidad para escribir cuando necesite

## Pruebas: `tests/test_neuroasistente_service.py`
- Respuesta "me duele más desde ayer" → clínica=True
- Respuesta "quiero cancelar la cita" → comercial=True
- Respuesta "sí, confirmo asistencia" → ambos False
