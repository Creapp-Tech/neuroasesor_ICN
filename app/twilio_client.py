"""Twilio WhatsApp client — outbound message delivery.

Uses the Twilio REST API to send WhatsApp messages in response to
inbound messages received at the /webhook/twilio endpoint.
"""

import logging

from app import config

logger = logging.getLogger(__name__)


def send_whatsapp_reply(to: str, body: str) -> bool:
    """Send a WhatsApp message via Twilio to the given phone number.

    `to` must be a plain E.164 number (e.g. '573001234567').
    The 'whatsapp:' prefix is added automatically.
    Returns True on success, False on any error (never raises).
    """
    try:
        from twilio.rest import Client  # lazy import — not needed in tests
        client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
        client.messages.create(
            from_=f"whatsapp:{config.TWILIO_WHATSAPP_FROM}",
            to=f"whatsapp:{to}",
            body=body,
        )
        logger.info("Twilio WhatsApp sent to %s (%d chars)", to, len(body))
        return True
    except Exception:
        logger.exception("Failed to send Twilio WhatsApp to %s", to)
        return False
