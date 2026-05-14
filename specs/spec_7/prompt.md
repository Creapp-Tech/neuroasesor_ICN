
# Prompt — Spec 7: whatsapp_client.py + manychat_client.py

Eres un Ingeniero de Backend Python especializado en integraciones con APIs de mensajería. Tu tarea es implementar los clientes de WhatsApp Business API y ManyChat para el sistema NeurOrientador de ICN Salud.

## Contexto
WhatsApp es el canal principal de conversación clínica (webhook 24/7). ManyChat actúa como panel de gestión del Neuroasesor y canal complementario. Todos los tokens están en `config.py`. Los specs anteriores ya están implementados.

## Entrega requerida

### Archivo 1: `whatsapp_client.py`
```python
def send_message(to: str, text: str) -> bool:
    """
    Envía mensaje de texto por WhatsApp Business API (Meta Cloud API).
    POST a https://graph.facebook.com/v18.0/{PHONE_ID}/messages
    Headers: Authorization Bearer {WHATSAPP_TOKEN}
    Body: {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
    Returns: True si status 200
    """

def parse_webhook(payload: dict) -> tuple[str, str, str]:
    """
    Parsea el cuerpo JSON del webhook de WhatsApp Business API.
    Returns: (numero_telefono, mensaje_texto, timestamp)
    Maneja la estructura anidada: entry[0].changes[0].value.messages[0]
    """

def verify_hmac(payload_raw: bytes, signature_header: str) -> bool:
    """
    Verifica firma X-Hub-Signature-256 del webhook.
    Usa config.WHATSAPP_WEBHOOK_SECRET como clave HMAC-SHA256.
    Returns: True si la firma es válida.
    """
```

### Archivo 2: `manychat_client.py`
```python
def update_contact_tag(telefono: str, tag: str) -> bool:
    """
    Actualiza etiqueta del contacto en ManyChat.
    Tags válidos: "nuevo", "en_orientacion", "agendado", "escalado", "cerrado"
    Usa ManyChat API v2.0 con config.MANYCHAT_API_TOKEN
    """

def assign_to_human(telefono: str, prioridad: str) -> bool:
    """
    Asigna conversación al agente humano (Neuroasesor) en ManyChat.
    prioridad: "agendado" | "particular" | "general"
    """

def mark_as_vencida(telefono: str) -> bool:
    """
    Marca conversación como vencida por incumplimiento de SLA.
    Usado cuando cumple_sla_15min = False.
    """
```

## Reglas de implementación
- Todos los requests HTTP con `httpx` (async compatible)
- Timeout de 10 segundos en todos los requests
- Logging de errores, no lanzar excepciones que rompan el flujo principal
- Si ManyChat falla, el flujo de WhatsApp debe continuar (ManyChat es complementario)
