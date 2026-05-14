"""Tests for app/audit_log.py.

All external I/O (Supabase) is mocked so tests run without network access
or real credentials.
"""

from unittest.mock import MagicMock, patch

import pytest

from app import config
from app.schemas import Conversacion, Paciente
from app.audit_log import (
    get_conversaciones_paciente,
    log_error_operativo,
    log_turno,
    update_historial,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def paciente():
    return Paciente(
        paciente_id="PAC-001",
        telefono="573001234567",
        nombre="María López",
        fase_actual="F3",
        historial_json=[],
    )


@pytest.fixture
def paciente_con_historial():
    historial = [
        {"role": "user", "content": f"mensaje {i}"}
        if i % 2 == 0
        else {"role": "assistant", "content": f"respuesta {i}"}
        for i in range(config.MAX_HISTORIAL_TURNOS)
    ]
    return Paciente(
        paciente_id="PAC-002",
        telefono="573001234568",
        fase_actual="F3",
        historial_json=historial,
    )


# ── log_turno ─────────────────────────────────────────────────────────────────

@patch("app.audit_log._get_repo")
class TestLogTurno:
    def test_returns_conversacion(self, mock_repo):
        mock_repo.return_value = MagicMock()
        result = log_turno(
            paciente_id="PAC-001",
            telefono="573001234567",
            fase="F3",
            mensaje_usuario="Tengo dolor de cabeza",
            respuesta_agente="Entiendo, cuéntame más.",
            guia_soporte_turno="guia_cefalea",
            tokens_usados=120,
            flag_alarma=False,
            escalado_humano=False,
            version_prompt="v6.0",
        )
        assert isinstance(result, Conversacion)
        assert result.paciente_id == "PAC-001"
        assert result.telefono == "573001234567"
        assert result.fase == "F3"

    def test_conv_id_starts_with_prefix(self, mock_repo):
        mock_repo.return_value = MagicMock()
        result = log_turno(
            paciente_id="PAC-001",
            telefono="573001234567",
            fase="F2",
            mensaje_usuario="Hola",
            respuesta_agente="Hola paciente",
            guia_soporte_turno=None,
            tokens_usados=50,
            flag_alarma=False,
            escalado_humano=False,
            version_prompt="v6.0",
        )
        assert result.conv_id.startswith("CONV-PAC-001-")

    def test_fields_stored_correctly(self, mock_repo):
        mock_repo.return_value = MagicMock()
        result = log_turno(
            paciente_id="PAC-001",
            telefono="573001234567",
            fase="F3",
            mensaje_usuario="Peor dolor de mi vida",
            respuesta_agente="Esto es urgente.",
            guia_soporte_turno="guia_urgencia",
            tokens_usados=200,
            flag_alarma=True,
            escalado_humano=True,
            version_prompt="v6.0",
        )
        assert result.tokens_usados == 200
        assert result.flag_alarma is True
        assert result.escalado_humano is True
        assert result.guia_soporte_turno == "guia_urgencia"
        assert result.version_prompt == "v6.0"

    def test_persists_to_repo(self, mock_repo):
        repo = MagicMock()
        mock_repo.return_value = repo
        log_turno(
            paciente_id="PAC-001",
            telefono="573001234567",
            fase="F1",
            mensaje_usuario="Hola",
            respuesta_agente="Bienvenido",
            guia_soporte_turno=None,
            tokens_usados=30,
            flag_alarma=False,
            escalado_humano=False,
            version_prompt="v6.0",
        )
        repo.insert_conversacion.assert_called_once()

    def test_repo_error_does_not_raise(self, mock_repo):
        repo = MagicMock()
        repo.insert_conversacion.side_effect = Exception("DB error")
        mock_repo.return_value = repo
        # Must not raise
        result = log_turno(
            paciente_id="PAC-001",
            telefono="573001234567",
            fase="F1",
            mensaje_usuario="Hola",
            respuesta_agente="Bienvenido",
            guia_soporte_turno=None,
            tokens_usados=30,
            flag_alarma=False,
            escalado_humano=False,
            version_prompt="v6.0",
        )
        assert result is not None

    def test_guia_soporte_none_allowed(self, mock_repo):
        mock_repo.return_value = MagicMock()
        result = log_turno(
            paciente_id="PAC-001",
            telefono="573001234567",
            fase="F0",
            mensaje_usuario="Hola",
            respuesta_agente="Hola",
            guia_soporte_turno=None,
            tokens_usados=20,
            flag_alarma=False,
            escalado_humano=False,
            version_prompt="v6.0",
        )
        assert result.guia_soporte_turno is None


# ── update_historial ──────────────────────────────────────────────────────────

class TestUpdateHistorial:
    def test_adds_user_and_assistant_entries(self, paciente):
        result = update_historial(paciente, "Hola", "Bienvenido")
        assert len(result) == 2
        assert result[0] == {"role": "user", "content": "Hola"}
        assert result[1] == {"role": "assistant", "content": "Bienvenido"}

    def test_does_not_mutate_original_historial(self, paciente):
        original_len = len(paciente.historial_json)
        update_historial(paciente, "Hola", "Bienvenido")
        assert len(paciente.historial_json) == original_len

    def test_appends_to_existing_historial(self, paciente):
        paciente.historial_json = [
            {"role": "user", "content": "Previo"},
            {"role": "assistant", "content": "Respuesta previa"},
        ]
        result = update_historial(paciente, "Nuevo", "Nueva respuesta")
        assert len(result) == 4
        assert result[-1]["content"] == "Nueva respuesta"

    def test_trims_at_max_historial_turnos(self, paciente):
        # Fill up to exactly MAX_HISTORIAL_TURNOS
        paciente.historial_json = [
            {"role": "user" if i % 2 == 0 else "assistant", "content": f"msg{i}"}
            for i in range(config.MAX_HISTORIAL_TURNOS)
        ]
        result = update_historial(paciente, "Extra", "Extra response")
        assert len(result) == config.MAX_HISTORIAL_TURNOS

    def test_trims_oldest_entries(self, paciente):
        paciente.historial_json = [
            {"role": "user" if i % 2 == 0 else "assistant", "content": f"msg{i}"}
            for i in range(config.MAX_HISTORIAL_TURNOS)
        ]
        result = update_historial(paciente, "Nuevo usuario", "Nueva respuesta")
        # Oldest entry (msg0) should be gone
        contents = [e["content"] for e in result]
        assert "msg0" not in contents
        assert "Nuevo usuario" in contents
        assert "Nueva respuesta" in contents

    def test_empty_historial_adds_two_entries(self, paciente):
        result = update_historial(paciente, "Primero", "Primera respuesta")
        assert len(result) == 2

    def test_below_max_no_trimming(self, paciente):
        paciente.historial_json = [
            {"role": "user", "content": "old1"},
            {"role": "assistant", "content": "old2"},
        ]
        result = update_historial(paciente, "new1", "new2")
        assert len(result) == 4

    def test_returns_list(self, paciente):
        result = update_historial(paciente, "Hola", "Hola")
        assert isinstance(result, list)


# ── log_error_operativo ───────────────────────────────────────────────────────

@patch("app.audit_log._get_repo")
class TestLogErrorOperativo:
    def test_updates_paciente_error_operativo(self, mock_repo):
        repo = MagicMock()
        mock_repo.return_value = repo
        log_error_operativo("PAC-001", "JSON inválido recibido del LLM", "json_invalido")
        repo.update_paciente_by_id.assert_called_once()
        call_args = repo.update_paciente_by_id.call_args
        assert call_args[0][0] == "PAC-001"
        assert "json_invalido" in call_args[0][1]["error_operativo"]

    def test_error_message_contains_tipo_and_description(self, mock_repo):
        repo = MagicMock()
        mock_repo.return_value = repo
        log_error_operativo("PAC-001", "Timeout conectando a Gemini", "api_error")
        campos = repo.update_paciente_by_id.call_args[0][1]
        assert "api_error" in campos["error_operativo"]
        assert "Timeout" in campos["error_operativo"]

    def test_repo_error_does_not_raise(self, mock_repo):
        repo = MagicMock()
        repo.update_paciente_by_id.side_effect = Exception("DB error")
        mock_repo.return_value = repo
        # Must not raise
        log_error_operativo("PAC-001", "DB failure", "db_error")

    def test_logs_at_error_level(self, mock_repo, caplog):
        mock_repo.return_value = MagicMock()
        import logging
        with caplog.at_level(logging.ERROR, logger="app.audit_log"):
            log_error_operativo("PAC-001", "Test error", "test_tipo")
        assert any("PAC-001" in r.message for r in caplog.records)


# ── get_conversaciones_paciente ───────────────────────────────────────────────

@patch("app.audit_log._get_repo")
class TestGetConversacionesPaciente:
    def _make_conv(self, conv_id: str) -> Conversacion:
        from datetime import timezone
        from datetime import datetime
        return Conversacion(
            conv_id=conv_id,
            paciente_id="PAC-001",
            telefono="573001234567",
            fase="F3",
            mensaje_usuario="Hola",
            respuesta_agente="Hola paciente",
            timestamp=datetime(2026, 5, 20, 10, 0, 0, tzinfo=timezone.utc),
        )

    def test_returns_list_of_conversaciones(self, mock_repo):
        repo = MagicMock()
        repo.get_conversaciones_by_paciente_id.return_value = [
            self._make_conv("CONV-PAC-001-001"),
            self._make_conv("CONV-PAC-001-002"),
        ]
        mock_repo.return_value = repo

        result = get_conversaciones_paciente("PAC-001")
        assert len(result) == 2
        assert all(isinstance(c, Conversacion) for c in result)

    def test_calls_repo_with_correct_id(self, mock_repo):
        repo = MagicMock()
        repo.get_conversaciones_by_paciente_id.return_value = []
        mock_repo.return_value = repo

        get_conversaciones_paciente("PAC-999")
        repo.get_conversaciones_by_paciente_id.assert_called_once_with("PAC-999")

    def test_empty_result_returns_empty_list(self, mock_repo):
        repo = MagicMock()
        repo.get_conversaciones_by_paciente_id.return_value = []
        mock_repo.return_value = repo

        result = get_conversaciones_paciente("PAC-001")
        assert result == []

    def test_repo_error_returns_empty_list(self, mock_repo):
        repo = MagicMock()
        repo.get_conversaciones_by_paciente_id.side_effect = Exception("DB error")
        mock_repo.return_value = repo

        result = get_conversaciones_paciente("PAC-001")
        assert result == []
