"""Tests for app/neuroasesor_service.py.

All external I/O (Supabase) is mocked so tests run without network access
or real credentials.
"""

from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch, call

import pytest

from app.schemas import Escalamiento, NeuroAsesorInteraccion
from app.neuroasesor_service import register_intervencion, record_escalamiento_atendido


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def escalamiento():
    ts = datetime(2026, 5, 20, 10, 0, 0, tzinfo=timezone.utc)
    return Escalamiento(
        escalamiento_id="ESC-PAC-001-20260520T100000",
        paciente_id="PAC-001",
        timestamp_escalamiento=ts,
        tipo_escalamiento="neuroasistente_clinico",
        motivo="Señal clínica detectada",
        prioridad_paciente="particular",
        fase_origen="NeuroAsistente",
    )


@pytest.fixture
def escalamiento_comercial():
    ts = datetime(2026, 5, 20, 10, 0, 0, tzinfo=timezone.utc)
    return Escalamiento(
        escalamiento_id="ESC-PAC-002-20260520T100000",
        paciente_id="PAC-002",
        timestamp_escalamiento=ts,
        tipo_escalamiento="neuroasistente_comercial",
        motivo="Señal comercial detectada",
        prioridad_paciente="particular",
        fase_origen="NeuroAsistente",
    )


@pytest.fixture
def escalamiento_alarma():
    ts = datetime(2026, 5, 20, 10, 0, 0, tzinfo=timezone.utc)
    return Escalamiento(
        escalamiento_id="ESC-PAC-003-20260520T100000",
        paciente_id="PAC-003",
        timestamp_escalamiento=ts,
        tipo_escalamiento="alarma_critica",
        motivo="Posible convulsión",
        prioridad_paciente="particular",
        fase_origen="F3",
    )


# ── register_intervencion ─────────────────────────────────────────────────────

@patch("app.neuroasesor_service._get_repo")
class TestRegisterIntervencion:
    def test_returns_interaccion(self, mock_repo):
        mock_repo.return_value = MagicMock()
        result = register_intervencion(
            paciente_id="PAC-001",
            tipo="escalamiento_clinico",
            canal="whatsapp",
            resumen="Atendí la consulta del paciente.",
            resultado="cerrado",
            responsable="Dr. Pérez",
        )
        assert isinstance(result, NeuroAsesorInteraccion)
        assert result.paciente_id == "PAC-001"
        assert result.tipo_interaccion == "escalamiento_clinico"
        assert result.resultado == "cerrado"
        assert result.responsable == "Dr. Pérez"

    def test_id_starts_with_prefix(self, mock_repo):
        mock_repo.return_value = MagicMock()
        result = register_intervencion(
            paciente_id="PAC-001",
            tipo="soporte",
            canal="telefono",
            resumen="Consulta sobre medicamento.",
            resultado="pendiente",
            responsable="Dra. García",
        )
        assert result.neuroasesor_interaccion_id.startswith("NA_H-PAC-001-")

    def test_persists_to_repo(self, mock_repo):
        repo = MagicMock()
        mock_repo.return_value = repo
        register_intervencion(
            paciente_id="PAC-001",
            tipo="contacto_proactivo",
            canal="whatsapp",
            resumen="Contacto de seguimiento.",
            resultado="cerrado",
            responsable="Asesor",
        )
        repo.insert_neuroasesor_interaccion.assert_called_once()

    def test_repo_error_does_not_raise(self, mock_repo):
        repo = MagicMock()
        repo.insert_neuroasesor_interaccion.side_effect = Exception("DB error")
        mock_repo.return_value = repo
        # Must not raise
        result = register_intervencion(
            paciente_id="PAC-001",
            tipo="soporte",
            canal="whatsapp",
            resumen="Soporte técnico.",
            resultado="cerrado",
            responsable="Sistema",
        )
        assert result is not None

    def test_optional_fields_stored(self, mock_repo):
        mock_repo.return_value = MagicMock()
        result = register_intervencion(
            paciente_id="PAC-001",
            tipo="cierre_comercial",
            canal="telefono",
            resumen="Cierre de programa.",
            resultado="nueva_cita_agendada",
            responsable="Asesor Comercial",
            oportunidad_detectada="nuevo_programa",
            incidencia="demora_agenda",
            notas_internas="Paciente interesado en programa de epilepsia",
        )
        assert result.oportunidad_detectada == "nuevo_programa"
        assert result.incidencia == "demora_agenda"
        assert result.notas_internas == "Paciente interesado en programa de epilepsia"


# ── record_escalamiento_atendido ──────────────────────────────────────────────

@patch("app.neuroasesor_service._get_repo")
class TestRecordEscalamientoAtendido:
    def test_updates_escalamiento_in_repo(self, mock_repo, escalamiento):
        repo = MagicMock()
        repo.get_escalamiento_by_id.return_value = escalamiento
        mock_repo.return_value = repo

        record_escalamiento_atendido(escalamiento.escalamiento_id, "Dr. Ramírez")

        repo.update_escalamiento.assert_called_once()
        call_args = repo.update_escalamiento.call_args
        assert call_args[0][0] == escalamiento.escalamiento_id
        campos = call_args[0][1]
        assert "timestamp_respuesta_humano" in campos
        assert "tiempo_respuesta_humano" in campos
        assert "cumple_sla_15min" in campos
        assert campos["responsable"] == "Dr. Ramírez"

    def test_creates_intervencion_record(self, mock_repo, escalamiento):
        repo = MagicMock()
        repo.get_escalamiento_by_id.return_value = escalamiento
        mock_repo.return_value = repo

        record_escalamiento_atendido(escalamiento.escalamiento_id, "Dr. Ramírez")

        repo.insert_neuroasesor_interaccion.assert_called_once()

    def test_clinical_escalamiento_creates_clinical_tipo(self, mock_repo, escalamiento):
        repo = MagicMock()
        repo.get_escalamiento_by_id.return_value = escalamiento
        mock_repo.return_value = repo

        record_escalamiento_atendido(escalamiento.escalamiento_id, "Dr. Ramírez")

        intervencion_arg = repo.insert_neuroasesor_interaccion.call_args[0][0]
        assert intervencion_arg.tipo_interaccion == "escalamiento_clinico"

    def test_commercial_escalamiento_creates_commercial_tipo(self, mock_repo, escalamiento_comercial):
        repo = MagicMock()
        repo.get_escalamiento_by_id.return_value = escalamiento_comercial
        mock_repo.return_value = repo

        record_escalamiento_atendido(escalamiento_comercial.escalamiento_id, "Asesor")

        intervencion_arg = repo.insert_neuroasesor_interaccion.call_args[0][0]
        assert intervencion_arg.tipo_interaccion == "escalamiento_comercial"

    def test_sla_compliance_within_limit(self, mock_repo, escalamiento):
        """Response within 15 min → cumple_sla True."""
        repo = MagicMock()
        repo.get_escalamiento_by_id.return_value = escalamiento
        mock_repo.return_value = repo

        # Patch _now_utc to return 10 minutes after escalamiento
        with patch("app.neuroasesor_service._now_utc") as mock_now:
            mock_now.return_value = escalamiento.timestamp_escalamiento + timedelta(minutes=10)
            record_escalamiento_atendido(escalamiento.escalamiento_id, "Dr. X")

        campos = repo.update_escalamiento.call_args[0][1]
        assert campos["cumple_sla_15min"] is True
        assert campos["tiempo_respuesta_humano"] == pytest.approx(10.0, abs=0.1)

    def test_sla_breach_beyond_limit(self, mock_repo, escalamiento):
        """Response after 20 min → cumple_sla False."""
        repo = MagicMock()
        repo.get_escalamiento_by_id.return_value = escalamiento
        mock_repo.return_value = repo

        with patch("app.neuroasesor_service._now_utc") as mock_now:
            mock_now.return_value = escalamiento.timestamp_escalamiento + timedelta(minutes=20)
            record_escalamiento_atendido(escalamiento.escalamiento_id, "Dr. X")

        campos = repo.update_escalamiento.call_args[0][1]
        assert campos["cumple_sla_15min"] is False

    def test_alarma_critica_uses_5min_sla(self, mock_repo, escalamiento_alarma):
        """alarma_critica SLA is 5 min, not 15."""
        repo = MagicMock()
        repo.get_escalamiento_by_id.return_value = escalamiento_alarma
        mock_repo.return_value = repo

        with patch("app.neuroasesor_service._now_utc") as mock_now:
            # 7 minutes → exceeds 5 min SLA
            mock_now.return_value = escalamiento_alarma.timestamp_escalamiento + timedelta(minutes=7)
            record_escalamiento_atendido(escalamiento_alarma.escalamiento_id, "Dr. X")

        campos = repo.update_escalamiento.call_args[0][1]
        assert campos["cumple_sla_15min"] is False

    def test_escalamiento_not_found_no_update(self, mock_repo):
        repo = MagicMock()
        repo.get_escalamiento_by_id.return_value = None
        mock_repo.return_value = repo

        record_escalamiento_atendido("NON-EXISTENT", "Dr. X")

        repo.update_escalamiento.assert_not_called()
        repo.insert_neuroasesor_interaccion.assert_not_called()

    def test_fetch_error_no_raise(self, mock_repo):
        repo = MagicMock()
        repo.get_escalamiento_by_id.side_effect = Exception("DB error")
        mock_repo.return_value = repo

        # Must not raise
        record_escalamiento_atendido("ESC-PAC-001-20260520T100000", "Dr. X")
        repo.update_escalamiento.assert_not_called()
