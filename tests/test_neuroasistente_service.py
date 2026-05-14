"""Tests for app/neuroasistente_service.py.

All external I/O (Supabase, WhatsApp, ManyChat) is mocked so tests run
without network access or real credentials.
"""

from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from app.schemas import Cita, NeuroAsistenteInteraccion, Paciente
from app.neuroasistente_service import (
    analyze_response,
    handle_no_response,
    process_patient_response,
    send_confirmacion_cita,
    send_preparacion_cita,
    send_recordatorio,
    send_seguimiento_post_cita,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def paciente():
    return Paciente(
        paciente_id="PAC-001",
        telefono="573001234567",
        nombre="María López",
        edad=45,
        ciudad="Bogotá",
        aseguramiento="Particular",
        consentimiento_datos_clinicos=True,
        consentimiento_teleorientacion=True,
        fase_actual="F4",
        programa_clinico="Cefalea",
        prioridad_operativa="particular",
    )


@pytest.fixture
def cita():
    return Cita(
        cita_id="CITA-001",
        paciente_id="PAC-001",
        tipo="consulta",
        programa="Cefalea",
        fecha_cita=date(2026, 5, 20),
        hora_cita="10:00 AM",
        canal_agenda="whatsapp",
        confirmacion="Pendiente",
        seguimiento_post=False,
    )


@pytest.fixture
def interaccion_enviada():
    from datetime import datetime, timezone
    return NeuroAsistenteInteraccion(
        interaccion_id="NA-PAC-001-20260520T100000-abc12345",
        paciente_id="PAC-001",
        cita_id="CITA-001",
        fecha_hora=datetime(2026, 5, 20, 10, 0, 0, tzinfo=timezone.utc),
        canal_contacto="whatsapp",
        tipo_interaccion="seguimiento_post_cita",
        mensaje_enviado="¿Cómo te fue?",
        estado_interaccion="enviado",
        requiere_revision_clinica=False,
        requiere_revision_comercial=False,
        responsable="NeuroAsistente_automatico",
        prioridad_paciente="particular",
        version_flujo="v6.0",
    )


# ── analyze_response — pure function, no mocks needed ────────────────────────

class TestAnalyzeResponse:
    def test_clinical_signal_pain_worse(self):
        clinica, comercial = analyze_response("me duele más desde ayer", "seguimiento_post_cita")
        assert clinica is True
        assert comercial is False

    def test_clinical_signal_complication(self):
        clinica, comercial = analyze_response("tuve una complicación después de la cita", "seguimiento_post_cita")
        assert clinica is True

    def test_clinical_signal_medication_doubt(self):
        clinica, comercial = analyze_response("tengo dudas sobre el medicamento que me recetaron", "seguimiento_post_cita")
        assert clinica is True

    def test_clinical_signal_anxiety(self):
        clinica, comercial = analyze_response("me siento con mucha angustia", "seguimiento_post_cita")
        assert clinica is True

    def test_commercial_signal_cancel(self):
        clinica, comercial = analyze_response("quiero cancelar la cita", "confirmacion_cita")
        assert clinica is False
        assert comercial is True

    def test_commercial_signal_reschedule(self):
        clinica, comercial = analyze_response("necesito reagendar para otro día", "recordatorio")
        assert comercial is True

    def test_commercial_signal_complaint(self):
        clinica, comercial = analyze_response("no quedé satisfecho con el servicio", "seguimiento_post_cita")
        assert comercial is True

    def test_commercial_signal_new_program(self):
        clinica, comercial = analyze_response("estoy interesado en otro programa también", "seguimiento_post_cita")
        assert comercial is True

    def test_normal_confirmation(self):
        clinica, comercial = analyze_response("sí, confirmo asistencia", "confirmacion_cita")
        assert clinica is False
        assert comercial is False

    def test_neutral_response(self):
        clinica, comercial = analyze_response("gracias, ahí estaré", "recordatorio")
        assert clinica is False
        assert comercial is False

    def test_empty_response(self):
        clinica, comercial = analyze_response("", "confirmacion_cita")
        assert clinica is False
        assert comercial is False


# ── send_* functions ──────────────────────────────────────────────────────────

@patch("app.neuroasistente_service._get_repo")
@patch("app.neuroasistente_service.send_message", return_value=True)
class TestSendFunctions:
    def test_send_confirmacion_cita_returns_interaccion(self, mock_wa, mock_repo, paciente, cita):
        mock_repo.return_value = MagicMock()
        result = send_confirmacion_cita(paciente, cita)
        assert result.tipo_interaccion == "confirmacion_cita"
        assert result.estado_interaccion == "enviado"
        assert result.paciente_id == "PAC-001"
        assert result.cita_id == "CITA-001"
        assert mock_wa.called

    def test_send_confirmacion_contains_fecha(self, mock_wa, mock_repo, paciente, cita):
        mock_repo.return_value = MagicMock()
        result = send_confirmacion_cita(paciente, cita)
        assert "20/05/2026" in result.mensaje_enviado

    def test_send_preparacion_cita(self, mock_wa, mock_repo, paciente, cita):
        mock_repo.return_value = MagicMock()
        result = send_preparacion_cita(paciente, cita)
        assert result.tipo_interaccion == "preparacion_cita"
        assert "Cefalea" in result.mensaje_enviado

    def test_send_recordatorio(self, mock_wa, mock_repo, paciente, cita):
        mock_repo.return_value = MagicMock()
        result = send_recordatorio(paciente, cita)
        assert result.tipo_interaccion == "recordatorio"
        assert "mañana" in result.mensaje_enviado

    def test_send_seguimiento_post_cita(self, mock_wa, mock_repo, paciente, cita):
        mock_repo.return_value = MagicMock()
        result = send_seguimiento_post_cita(paciente, cita)
        assert result.tipo_interaccion == "seguimiento_post_cita"
        assert "ayer" in result.mensaje_enviado

    def test_send_marks_pendiente_when_whatsapp_fails(self, mock_wa, mock_repo, paciente, cita):
        mock_wa.return_value = False
        mock_repo.return_value = MagicMock()
        result = send_confirmacion_cita(paciente, cita)
        assert result.estado_interaccion == "pendiente"

    def test_interaccion_id_starts_with_prefix(self, mock_wa, mock_repo, paciente, cita):
        mock_repo.return_value = MagicMock()
        result = send_confirmacion_cita(paciente, cita)
        assert result.interaccion_id.startswith("NA-PAC-001-")


# ── process_patient_response ──────────────────────────────────────────────────

@patch("app.neuroasistente_service._get_repo")
@patch("app.neuroasistente_service.send_message", return_value=True)
@patch("app.neuroasistente_service.update_contact_tag", return_value=True)
@patch("app.neuroasistente_service.assign_to_human", return_value=True)
class TestProcessPatientResponse:
    def test_normal_response_no_escalation(self, mock_assign, mock_tag, mock_wa, mock_repo, interaccion_enviada):
        repo = MagicMock()
        repo.get_neuroasistente_interaccion_by_id.return_value = interaccion_enviada
        mock_repo.return_value = repo

        process_patient_response(interaccion_enviada.interaccion_id, "sí, confirmo asistencia")

        update_call_args = repo.update_neuroasistente_interaccion.call_args
        campos = update_call_args[0][1]
        assert campos["estado_interaccion"] == "respondido"
        assert campos["requiere_revision_clinica"] is False
        assert campos["requiere_revision_comercial"] is False
        # No escalation — WhatsApp Neuroasesor NOT called
        mock_wa.assert_not_called()

    def test_clinical_response_triggers_escalation(self, mock_assign, mock_tag, mock_wa, mock_repo, interaccion_enviada):
        repo = MagicMock()
        repo.get_neuroasistente_interaccion_by_id.return_value = interaccion_enviada
        mock_repo.return_value = repo

        process_patient_response(interaccion_enviada.interaccion_id, "me duele más desde ayer")

        campos = repo.update_neuroasistente_interaccion.call_args[0][1]
        assert campos["requiere_revision_clinica"] is True
        # Escalation WhatsApp was sent
        mock_wa.assert_called_once()
        notif_msg = mock_wa.call_args[0][1]
        assert "CLÍNICO" in notif_msg

    def test_commercial_response_triggers_escalation(self, mock_assign, mock_tag, mock_wa, mock_repo, interaccion_enviada):
        repo = MagicMock()
        repo.get_neuroasistente_interaccion_by_id.return_value = interaccion_enviada
        mock_repo.return_value = repo

        process_patient_response(interaccion_enviada.interaccion_id, "quiero cancelar la cita")

        campos = repo.update_neuroasistente_interaccion.call_args[0][1]
        assert campos["requiere_revision_comercial"] is True
        mock_wa.assert_called_once()
        notif_msg = mock_wa.call_args[0][1]
        assert "COMERCIAL" in notif_msg

    def test_interaccion_not_found_logs_and_returns(self, mock_assign, mock_tag, mock_wa, mock_repo):
        repo = MagicMock()
        repo.get_neuroasistente_interaccion_by_id.return_value = None
        mock_repo.return_value = repo

        # Must not raise
        process_patient_response("NON-EXISTENT-ID", "respuesta")
        repo.update_neuroasistente_interaccion.assert_not_called()


# ── handle_no_response ────────────────────────────────────────────────────────

@patch("app.neuroasistente_service._get_repo")
class TestHandleNoResponse:
    def test_24h_sets_pendiente(self, mock_repo):
        repo = MagicMock()
        mock_repo.return_value = repo

        handle_no_response("NA-PAC-001-test", 24)

        campos = repo.update_neuroasistente_interaccion.call_args[0][1]
        assert campos["estado_interaccion"] == "pendiente"

    def test_48h_also_pendiente(self, mock_repo):
        repo = MagicMock()
        mock_repo.return_value = repo

        handle_no_response("NA-PAC-001-test", 48)

        campos = repo.update_neuroasistente_interaccion.call_args[0][1]
        assert campos["estado_interaccion"] == "pendiente"

    def test_72h_sets_cerrado(self, mock_repo):
        repo = MagicMock()
        mock_repo.return_value = repo

        handle_no_response("NA-PAC-001-test", 72)

        campos = repo.update_neuroasistente_interaccion.call_args[0][1]
        assert campos["estado_interaccion"] == "cerrado"
        assert "2 intentos" in campos["notas_internas"]

    def test_less_than_24h_no_update(self, mock_repo):
        repo = MagicMock()
        mock_repo.return_value = repo

        handle_no_response("NA-PAC-001-test", 12)

        repo.update_neuroasistente_interaccion.assert_not_called()
