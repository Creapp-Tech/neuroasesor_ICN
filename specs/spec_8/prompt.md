# Prompt — Spec 8: escalation_service.py

Eres un Ingeniero de Backend Python con experiencia en sistemas de salud con SLAs críticos. Tu tarea es implementar el servicio de escalamiento humano y medición de SLA para NeurOrientador de ICN Salud.

## Contexto
El Neuroasesor tiene máximo 15 minutos para responder escalamientos. Alarmas críticas tienen objetivo de 5 minutos. El SLA se mide automáticamente. El incumplimiento genera alertas al coordinador ICN y marca conversaciones como vencidas. Los specs anteriores ya están implementados.

## Tipos de escalamiento y tiempos objetivo (del documento V6)
```
alarma_critica         → < 5 min (convulsión activa, ACV, suicidio)
clinico                → ≤ 15 min (banderas rojas en F3)
comercial              → ≤ 15 min (duda repetida en F4)
solicitud_paciente     → ≤ 15 min (pide hablar con persona)
error_sistema          → ≤ 15 min (JSON persistente)
neuroasistente_clinico → ≤ 15 min (señal post-cita)
neuroasistente_comercial → ≤ 30 min (cancelación, interés nuevo programa)
```

## Entrega requerida: `escalation_service.py`

```python
def create_escalamiento(
    paciente: Paciente, 
    tipo: str,  # de la lista de tipos
    motivo: str,
    fase_origen: str
) -> Escalamiento:
    """
    Crea registro de escalamiento en ESCALAMIENTOS.
    escalamiento_id = f"ESC-{paciente.paciente_id}-{timestamp_iso}"
    prioridad_paciente copiada de paciente.prioridad_operativa
    """

def notify_neuroasesor(
    escalamiento: Escalamiento, 
    paciente: Paciente,
    notas_clinicas: str  # notas_internas del último turno de F3
) -> None:
    """
    Notifica al Neuroasesor con TODOS los datos obligatorios:
    Nombre, teléfono, problema principal, nivel_riesgo, 
    resumen clínico, motivo, prioridad, fase_origen.
    
    Enviar por WhatsApp a config.ICN_NEUROASESOR_WHATSAPP.
    Llamar manychat_client.assign_to_human() con la prioridad.
    """

def register_human_response(escalamiento_id: str) -> float:
    """
    Registra que el Neuroasesor respondió.
    timestamp_respuesta_humano = now() Colombia timezone
    tiempo_respuesta_humano = minutos transcurridos desde timestamp_escalamiento
    Actualiza registro en ESCALAMIENTOS.
    Llama check_sla_compliance() y retorna minutos.
    """

def check_sla_compliance(escalamiento: Escalamiento) -> bool:
    """
    Calcula cumple_sla_15min según tipo.
    Actualiza campo en ESCALAMIENTOS.
    Si False: llama handle_sla_breach().
    """

def handle_sla_breach(escalamiento: Escalamiento, paciente: Paciente) -> None:
    """
    Acciones ante SLA incumplido:
    1. Registrar cumple_sla_15min=False en ESCALAMIENTOS
    2. Alertar coordinador ICN (config.ICN_COORDINADOR_WHATSAPP)
    3. manychat_client.mark_as_vencida(paciente.telefono)
    4. Registrar incidencia (para resumen diario)
    """

def trigger_alarm_escalamiento(
    paciente: Paciente, 
    motivo_alarma: str,
    notas: str
) -> Escalamiento:
    """
    Flujo completo para alarma clínica crítica:
    1. NO llamar al LLM (ya validado en alarm_filter)
    2. Enviar al paciente mensaje de orientación a urgencias + datos ICN
    3. Crear escalamiento tipo=alarma_critica
    4. Notificar Neuroasesor inmediatamente
    5. Retornar escalamiento creado
    """
```

## Mensaje obligatorio al paciente en alarma crítica
"⚠️ Por la urgencia de lo que describes, te recomendamos acudir a urgencias de inmediato o llamar a la línea de emergencias. Un asesor de ICN Salud también fue notificado y te contactará en los próximos minutos. Contacto ICN: [config.ICN_NEUROASESOR_WHATSAPP]"

## Pruebas: `tests/test_escalation_service.py`
- Escalamiento respondido en 10 min → cumple_sla_15min=True
- Escalamiento respondido en 20 min → cumple_sla_15min=False → handle_sla_breach llamado
- Alarma crítica → SLA objetivo es 5 min (no 15)
