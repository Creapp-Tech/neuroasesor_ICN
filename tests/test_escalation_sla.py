"""Tests for SLA compliance in escalamiento handling.

Exercises record_escalamiento_atendido from neuroasesor_service.
All Supabase I/O is mocked.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest

from app import config
from app.schemas import Escalamiento
from app.neuroasesor_service import record_escalamiento_atendido


def _make_escalamiento(tipo: str = "neuroasistente_clinico") -> Escalamiento:
    ts = datetime(2026, 5, 20, 10, 0, 0, tzinfo=timezone.utc)
    return Escalamiento(
        escalamiento_id="ESC-PAC-SLA-20260520T100000",
        paciente_id="PAC-SLA-001",
        timestamp_escalamiento=ts,
        tipo_escalamiento=tipo,
        motivo="Señal clínica detectada",
        prioridad_paciente="particular",
        fase_origen="NeuroAsistente",
    )


@patch("app.neuroasesor_service._get_repo")
class TestEscalamientoSLA:
    def test_sla_cumplido_10_minutos(self, mock_repo):
        """Response within 10 min → cumple_sla_15min = True."""
        esc = _make_escalamiento()
        repo = MagicMock()
        repo.get_escalamiento_by_id.return_value = esc
        mock_repo.return_value = repo

        with patch("app.neuroasesor_service._now_utc") as mock_now:
            mock_now.return_value = esc.timestamp_escalamiento + timedelta(minutes=10)
            record_escalamiento_atendido(esc.escalamiento_id, "Dr. Test")

        campos = repo.update_escalamiento.call_args[0][1]
        assert campos["cumple_sla_15min"] is True
        assert campos["tiempo_respuesta_humano"] == pytest.approx(10.0, abs=0.1)

    def test_sla_vencido_20_minutos(self, mock_repo):
        """Response after 20 min → cumple_sla_15min = False (SLA breached)."""
        esc = _make_escalamiento()
        repo = MagicMock()
        repo.get_escalamiento_by_id.return_value = esc
        mock_repo.return_value = repo

        with patch("app.neuroasesor_service._now_utc") as mock_now:
            mock_now.return_value = esc.timestamp_escalamiento + timedelta(minutes=20)
            record_escalamiento_atendido(esc.escalamiento_id, "Dr. Test")

        campos = repo.update_escalamiento.call_args[0][1]
        assert campos["cumple_sla_15min"] is False
        assert campos["tiempo_respuesta_humano"] == pytest.approx(20.0, abs=0.1)

    def test_alarma_critica_sla_5_min_cumplido(self, mock_repo):
        """alarma_critica within 4 min → cumple_sla = True (threshold is 5 min)."""
        esc = _make_escalamiento(tipo="alarma_critica")
        repo = MagicMock()
        repo.get_escalamiento_by_id.return_value = esc
        mock_repo.return_value = repo

        with patch("app.neuroasesor_service._now_utc") as mock_now:
            mock_now.return_value = esc.timestamp_escalamiento + timedelta(minutes=4)
            record_escalamiento_atendido(esc.escalamiento_id, "Dr. Test")

        campos = repo.update_escalamiento.call_args[0][1]
        assert campos["cumple_sla_15min"] is True

    def test_alarma_critica_sla_5_min_vencido(self, mock_repo):
        """alarma_critica after 7 min → cumple_sla = False (exceeds 5 min threshold)."""
        esc = _make_escalamiento(tipo="alarma_critica")
        repo = MagicMock()
        repo.get_escalamiento_by_id.return_value = esc
        mock_repo.return_value = repo

        with patch("app.neuroasesor_service._now_utc") as mock_now:
            mock_now.return_value = esc.timestamp_escalamiento + timedelta(minutes=7)
            record_escalamiento_atendido(esc.escalamiento_id, "Dr. Test")

        campos = repo.update_escalamiento.call_args[0][1]
        assert campos["cumple_sla_15min"] is False

    def test_sla_limite_exacto_15_minutos(self, mock_repo):
        """Response at exactly 15 min → cumple_sla = True (boundary)."""
        esc = _make_escalamiento()
        repo = MagicMock()
        repo.get_escalamiento_by_id.return_value = esc
        mock_repo.return_value = repo

        with patch("app.neuroasesor_service._now_utc") as mock_now:
            mock_now.return_value = esc.timestamp_escalamiento + timedelta(minutes=15)
            record_escalamiento_atendido(esc.escalamiento_id, "Dr. Test")

        campos = repo.update_escalamiento.call_args[0][1]
        assert campos["cumple_sla_15min"] is True

    def test_sla_config_minutos_usado(self, mock_repo):
        """SLA threshold matches config.SLA_MINUTOS (15 min) for regular escalations."""
        assert config.SLA_MINUTOS == 15
        assert config.SLA_ALARMA_MINUTOS == 5

    def test_update_registra_responsable(self, mock_repo):
        """The responsible Neuroasesor name is saved in the update."""
        esc = _make_escalamiento()
        repo = MagicMock()
        repo.get_escalamiento_by_id.return_value = esc
        mock_repo.return_value = repo

        with patch("app.neuroasesor_service._now_utc") as mock_now:
            mock_now.return_value = esc.timestamp_escalamiento + timedelta(minutes=8)
            record_escalamiento_atendido(esc.escalamiento_id, "Dra. Ramírez")

        campos = repo.update_escalamiento.call_args[0][1]
        assert campos["responsable"] == "Dra. Ramírez"
        assert "timestamp_respuesta_humano" in campos
