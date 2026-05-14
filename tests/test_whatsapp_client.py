"""Tests for app/whatsapp_client.py.

HTTP calls are intercepted with unittest.mock so no real network requests are made.
"""

import hashlib
import hmac
from unittest.mock import MagicMock, patch

import pytest

from app.whatsapp_client import parse_webhook, send_message, verify_hmac


# ── Helpers ──────────────────────────────────────────────────────────────────

def _mock_http_client(status_code: int, text: str = "") -> MagicMock:
    """Return a MagicMock that behaves like an httpx.Client context manager."""
    response = MagicMock()
    response.status_code = status_code
    response.text = text

    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    client.post.return_value = response
    return client


# ── send_message ─────────────────────────────────────────────────────────────

@patch("app.whatsapp_client.httpx.Client")
def test_send_message_success(mock_client_class):
    mock_client_class.return_value = _mock_http_client(200)
    assert send_message("573001234567", "Hola paciente") is True


@patch("app.whatsapp_client.httpx.Client")
def test_send_message_api_error(mock_client_class):
    mock_client_class.return_value = _mock_http_client(400, "Bad Request")
    assert send_message("573001234567", "Hola") is False


@patch("app.whatsapp_client.httpx.Client")
def test_send_message_network_exception(mock_client_class):
    client = MagicMock()
    client.__enter__ = MagicMock(side_effect=Exception("timeout"))
    client.__exit__ = MagicMock(return_value=False)
    mock_client_class.return_value = client
    # Must not raise — returns False on any exception
    assert send_message("573001234567", "Hola") is False


# ── parse_webhook ─────────────────────────────────────────────────────────────

def test_parse_webhook_valid():
    payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "573001234567",
                        "text": {"body": "Hola, tengo migraña"},
                        "timestamp": "1700000000",
                    }]
                }
            }]
        }]
    }
    result = parse_webhook(payload)
    assert result is not None
    telefono, texto, ts = result
    assert telefono == "573001234567"
    assert texto == "Hola, tengo migraña"
    assert ts == "1700000000"


def test_parse_webhook_no_messages():
    payload = {
        "entry": [{
            "changes": [{
                "value": {"messages": []}
            }]
        }]
    }
    assert parse_webhook(payload) is None


def test_parse_webhook_empty_payload():
    assert parse_webhook({}) is None


def test_parse_webhook_missing_entry():
    assert parse_webhook({"object": "whatsapp_business_account"}) is None


def test_parse_webhook_status_update_no_text():
    """Delivery receipts / status updates have no 'messages' key."""
    payload = {
        "entry": [{
            "changes": [{
                "value": {"statuses": [{"id": "mid123", "status": "delivered"}]}
            }]
        }]
    }
    assert parse_webhook(payload) is None


# ── verify_hmac ───────────────────────────────────────────────────────────────

def test_verify_hmac_valid():
    payload = b'{"entry": []}'
    secret = "placeholder"  # matches .env WHATSAPP_WEBHOOK_SECRET

    expected_digest = "sha256=" + hmac.new(
        secret.encode("utf-8"), payload, hashlib.sha256
    ).hexdigest()

    assert verify_hmac(payload, expected_digest) is True


def test_verify_hmac_wrong_signature():
    payload = b'{"entry": []}'
    assert verify_hmac(payload, "sha256=deadbeef") is False


def test_verify_hmac_tampered_payload():
    payload = b'{"entry": []}'
    secret = "placeholder"

    # Compute signature for original payload, then verify against tampered one
    original_sig = "sha256=" + hmac.new(
        secret.encode("utf-8"), payload, hashlib.sha256
    ).hexdigest()

    tampered = b'{"entry": [{"evil": true}]}'
    assert verify_hmac(tampered, original_sig) is False


@patch("app.whatsapp_client.WHATSAPP_WEBHOOK_SECRET", "")
def test_verify_hmac_missing_secret():
    assert verify_hmac(b"payload", "sha256=anything") is False
