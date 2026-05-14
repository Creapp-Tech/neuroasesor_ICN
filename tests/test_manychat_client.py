"""Tests for app/manychat_client.py.

HTTP calls are intercepted with unittest.mock. ManyChat failures must never
raise — the client always returns True/False.
"""

from unittest.mock import MagicMock, call, patch

import pytest

from app.manychat_client import (
    VALID_TAGS,
    assign_to_human,
    mark_as_vencida,
    update_contact_tag,
)

TELEFONO = "573001234567"


# ── Helpers ──────────────────────────────────────────────────────────────────

def _mock_http_client(status_code: int, text: str = "") -> MagicMock:
    response = MagicMock()
    response.status_code = status_code
    response.text = text

    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    client.post.return_value = response
    return client


# ── update_contact_tag ────────────────────────────────────────────────────────

@patch("app.manychat_client.httpx.Client")
def test_update_contact_tag_success(mock_client_class):
    mock_client_class.return_value = _mock_http_client(200)
    assert update_contact_tag(TELEFONO, "escalado") is True


@patch("app.manychat_client.httpx.Client")
def test_update_contact_tag_all_valid_tags(mock_client_class):
    mock_client_class.return_value = _mock_http_client(200)
    for tag in VALID_TAGS:
        assert update_contact_tag(TELEFONO, tag) is True


@patch("app.manychat_client.httpx.Client")
def test_update_contact_tag_api_error(mock_client_class):
    mock_client_class.return_value = _mock_http_client(400, "Bad Request")
    assert update_contact_tag(TELEFONO, "agendado") is False


def test_update_contact_tag_invalid_tag():
    """Invalid tag must fail immediately without making any HTTP call."""
    assert update_contact_tag(TELEFONO, "invalido") is False


@patch("app.manychat_client.httpx.Client")
def test_update_contact_tag_network_exception(mock_client_class):
    client = MagicMock()
    client.__enter__ = MagicMock(side_effect=Exception("network error"))
    client.__exit__ = MagicMock(return_value=False)
    mock_client_class.return_value = client
    assert update_contact_tag(TELEFONO, "escalado") is False


# ── assign_to_human ───────────────────────────────────────────────────────────

@patch("app.manychat_client.httpx.Client")
def test_assign_to_human_success(mock_client_class):
    """Both the tag call and the field call must succeed → True."""
    mock_client_class.return_value = _mock_http_client(200)
    assert assign_to_human(TELEFONO, "particular") is True


@patch("app.manychat_client.httpx.Client")
def test_assign_to_human_tag_fails(mock_client_class):
    """If the tag call fails, the function returns False."""
    mock_client_class.return_value = _mock_http_client(500, "Server Error")
    assert assign_to_human(TELEFONO, "agendado") is False


@patch("app.manychat_client.httpx.Client")
def test_assign_to_human_all_priorities(mock_client_class):
    mock_client_class.return_value = _mock_http_client(200)
    for prioridad in ("agendado", "particular", "general"):
        assert assign_to_human(TELEFONO, prioridad) is True


# ── mark_as_vencida ────────────────────────────────────────────────────────────

@patch("app.manychat_client.httpx.Client")
def test_mark_as_vencida_success(mock_client_class):
    mock_client_class.return_value = _mock_http_client(201)
    assert mark_as_vencida(TELEFONO) is True


@patch("app.manychat_client.httpx.Client")
def test_mark_as_vencida_api_error(mock_client_class):
    mock_client_class.return_value = _mock_http_client(503, "Service Unavailable")
    assert mark_as_vencida(TELEFONO) is False


@patch("app.manychat_client.httpx.Client")
def test_mark_as_vencida_exception(mock_client_class):
    client = MagicMock()
    client.__enter__ = MagicMock(side_effect=Exception("timeout"))
    client.__exit__ = MagicMock(return_value=False)
    mock_client_class.return_value = client
    assert mark_as_vencida(TELEFONO) is False
