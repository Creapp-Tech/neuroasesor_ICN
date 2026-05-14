"""WhatsApp Business API client for NeurOrientador.

Handles sending messages via Meta Cloud API, parsing inbound webhook payloads,
and verifying HMAC signatures. Uses httpx with a 10-second timeout.
"""

import hashlib
import hmac
import logging
from typing import Optional

import httpx

from app.config import (
    WHATSAPP_PHONE_ID,
    WHATSAPP_TOKEN,
    WHATSAPP_WEBHOOK_SECRET,
)

logger = logging.getLogger(__name__)

WHATSAPP_API_URL = "https://graph.facebook.com/v18.0/{phone_id}/messages"
TIMEOUT_SECONDS = 10


def send_message(to: str, text: str) -> bool:
    """
    Envía mensaje de texto por WhatsApp Business API (Meta Cloud API).
    POST a https://graph.facebook.com/v18.0/{PHONE_ID}/messages
    Headers: Authorization Bearer {WHATSAPP_TOKEN}
    Body: {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
    Returns: True si status 200
    """
    url = WHATSAPP_API_URL.format(phone_id=WHATSAPP_PHONE_ID)
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    body = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

    try:
        with httpx.Client(timeout=TIMEOUT_SECONDS) as client:
            response = client.post(url, json=body, headers=headers)

        if response.status_code == 200:
            logger.info("WhatsApp message sent successfully to %s", to)
            return True
        else:
            logger.error(
                "WhatsApp API error: status=%d, body=%s",
                response.status_code,
                response.text,
            )
            return False
    except Exception:
        logger.exception("Failed to send WhatsApp message to %s", to)
        return False


def parse_webhook(payload: dict) -> Optional[tuple[str, str, str]]:
    """
    Parsea el cuerpo JSON del webhook de WhatsApp Business API.
    Returns: (numero_telefono, mensaje_texto, timestamp) o None si no se puede parsear.
    Maneja la estructura anidada: entry[0].changes[0].value.messages[0]
    """
    try:
        entry = payload.get("entry", [None])[0]
        if entry is None:
            return None

        change = entry.get("changes", [None])[0]
        if change is None:
            return None

        value = change.get("value", {})
        messages = value.get("messages", [None])[0]
        if messages is None:
            return None

        numero_telefono = messages.get("from", "")
        mensaje_texto = messages.get("text", {}).get("body", "")
        timestamp = str(messages.get("timestamp", ""))

        return numero_telefono, mensaje_texto, timestamp
    except Exception:
        logger.exception("Error parsing WhatsApp webhook payload")
        return None


def verify_hmac(payload_raw: bytes, signature_header: str) -> bool:
    """
    Verifica firma X-Hub-Signature-256 del webhook.
    Usa config.WHATSAPP_WEBHOOK_SECRET como clave HMAC-SHA256.
    Returns: True si la firma es válida.
    """
    if not WHATSAPP_WEBHOOK_SECRET:
        logger.error("WHATSAPP_WEBHOOK_SECRET is not set")
        return False

    try:
        expected = "sha256=" + hmac.new(
            WHATSAPP_WEBHOOK_SECRET.encode("utf-8"),
            payload_raw,
            hashlib.sha256,
        ).hexdigest()

        result = hmac.compare_digest(expected, signature_header)
        if not result:
            logger.warning("WhatsApp webhook HMAC verification failed")
        return result
    except Exception:
        logger.exception("Error verifying WhatsApp webhook HMAC")
        return False