"""ManyChat API client for NeurOrientador.

Manages contact tags, human agent assignment, and SLA breach marking.
All calls use the ManyChat subscriber-by-phone endpoints so no subscriber ID
lookup is needed. Errors are logged but never re-raised — ManyChat is
complementary and must not break the WhatsApp conversation flow.
"""

import logging

import httpx

from app.config import MANYCHAT_API_TOKEN

logger = logging.getLogger(__name__)

_BASE_URL = "https://api.manychat.com"
_TIMEOUT = 10  # seconds

# Tags recognised by ManyChat flows in this integration
VALID_TAGS = {"nuevo", "en_orientacion", "agendado", "escalado", "cerrado"}


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {MANYCHAT_API_TOKEN}",
        "Content-Type": "application/json",
    }


def _post(url: str, payload: dict) -> bool:
    """Shared helper: POST to ManyChat, return True on 200/201."""
    try:
        with httpx.Client(timeout=_TIMEOUT) as client:
            response = client.post(url, json=payload, headers=_headers())
        if response.status_code in (200, 201):
            return True
        logger.error(
            "ManyChat error: POST %s status=%d body=%s",
            url,
            response.status_code,
            response.text,
        )
        return False
    except Exception:
        logger.exception("ManyChat request failed: POST %s", url)
        return False


def update_contact_tag(telefono: str, tag: str) -> bool:
    """
    Añade una etiqueta al contacto por número de teléfono.
    Tags válidos: "nuevo", "en_orientacion", "agendado", "escalado", "cerrado".
    Retorna False (sin excepción) si el tag no es válido o la llamada falla.
    """
    if tag not in VALID_TAGS:
        logger.error("Invalid ManyChat tag '%s'. Valid: %s", tag, VALID_TAGS)
        return False

    url = f"{_BASE_URL}/fb/subscriber/addTagByPhone"
    payload = {"phone": telefono, "tag_name": tag}
    success = _post(url, payload)
    if success:
        logger.info("ManyChat tag '%s' applied to %s", tag, telefono)
    return success


def assign_to_human(telefono: str, prioridad: str) -> bool:
    """
    Asigna la conversación al Neuroasesor humano en ManyChat.
    - Añade la etiqueta "escalado"
    - Registra la prioridad en un campo personalizado
    prioridad: "agendado" | "particular" | "general"
    """
    # 1. Tag de escalamiento
    tag_ok = update_contact_tag(telefono, "escalado")

    # 2. Campo personalizado con prioridad operativa
    url = f"{_BASE_URL}/fb/subscriber/setCustomFieldByPhone"
    payload = {
        "phone": telefono,
        "field_name": "prioridad_atencion",
        "field_value": prioridad,
    }
    field_ok = _post(url, payload)
    if field_ok:
        logger.info("ManyChat assigned human for %s (prioridad=%s)", telefono, prioridad)

    return tag_ok and field_ok


def mark_as_vencida(telefono: str) -> bool:
    """
    Marca la conversación como vencida por incumplimiento de SLA.
    Establece el campo personalizado 'sla_status' = 'vencida'.
    """
    url = f"{_BASE_URL}/fb/subscriber/setCustomFieldByPhone"
    payload = {
        "phone": telefono,
        "field_name": "sla_status",
        "field_value": "vencida",
    }
    success = _post(url, payload)
    if success:
        logger.info("ManyChat SLA vencida marked for %s", telefono)
    return success
