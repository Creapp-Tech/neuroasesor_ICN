"""Tests for app/daily_reports.py.

All external I/O (Supabase, WhatsApp, LLM) is mocked so tests run without
network access or real credentials.
"""

from datetime import date, datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from app.schemas import Escalamiento, NeuroAsistenteInteraccion, ResumenDiario
from app.daily_reports import generate_daily_summary, send_daily_summary


# ── Helpers ──────────────────────────────────────────────────────────────────

def _make_interaccion(
    estado: str = "respondido",
    clinica: bool = False,
    comercial: bool = False,
) -> NeuroAsistenteInteraccion:
    return NeuroAsistenteInteraccion(
        interaccion_id=f"NA-PAC-001-20260520T100000-{estado[:3]}",
        paciente_id="PAC-001",
        fecha_hora=datetime(2026, 5, 20, 10, 0, 0, tzinfo=timezone.utc),
        canal_contacto="whatsapp",
        tipo_interaccion="seguimiento_post_cita",
        mensaje_enviado="¿Cómo te fue?",
        estado_interaccion=estado,
        requiere_revision_clinica=clinica,
        requiere_revision_comercial=comercial,
        responsable="NeuroAsistente_automatico",
    )


def _make_escalamiento(
    tiempo_respuesta: float = 10.0,
    cumple_sla: bool = True,
) -> Escalamiento:
    return Escalamiento(
        escalamiento_id="ESC-PAC-001-20260520T100000",
        paciente_id="PAC-001",
        timestamp_escalamiento=datetime(2026, 5, 20, 10, 0, 0, tzinfo=timezone.utc),
        tipo_escalamiento="neuroasistente_clinico",
        motivo="Señal clínica",
        tiempo_respuesta_humano=tiempo_respuesta,
        cumple_sla_15min=cumple_sla,
    )


# ── generate_daily_summary ────────────────────────────────────────────────────

@patch("app.daily_reports._generate_narrative", return_value="Resumen de prueba.")
@patch("app.daily_reports._get_repo")
class TestGenerateDailySummary:
    def test_counts_total_interacciones(self, mock_repo, mock_narr):
        repo = MagicMock()
        repo.get_interacciones_del_dia.return_value = [
            _make_interaccion("respondido"),
            _make_interaccion("enviado"),
            _make_interaccion("cerrado"),
        ]
        repo.get_escalamientos_del_dia.return_value = []
        mock_repo.return_value = repo

        result = generate_daily_summary(date(2026, 5, 20))
        assert result.total_interacciones_na == 3

    def test_counts_respondidas(self, mock_repo, mock_narr):
        repo = MagicMock()
        repo.get_interacciones_del_dia.return_value = [
            _make_interaccion("respondido"),
            _make_interaccion("respondido"),
            _make_interaccion("enviado"),
        ]
        repo.get_escalamientos_del_dia.return_value = []
        mock_repo.return_value = repo

        result = generate_daily_summary(date(2026, 5, 20))
        assert result.total_respondidas == 2

    def test_counts_sin_respuesta_as_cerrado(self, mock_repo, mock_narr):
        repo = MagicMock()
        repo.get_interacciones_del_dia.return_value = [
            _make_interaccion("cerrado"),
            _make_interaccion("cerrado"),
            _make_interaccion("respondido"),
        ]
        repo.get_escalamientos_del_dia.return_value = []
        mock_repo.return_value = repo

        result = generate_daily_summary(date(2026, 5, 20))
        assert result.total_sin_respuesta == 2

    def test_counts_clinicas(self, mock_repo, mock_narr):
        repo = MagicMock()
        repo.get_interacciones_del_dia.return_value = [
            _make_interaccion("respondido", clinica=True),
            _make_interaccion("respondido", clinica=False),
            _make_interaccion("respondido", clinica=True),
        ]
        repo.get_escalamientos_del_dia.return_value = []
        mock_repo.return_value = repo

        result = generate_daily_summary(date(2026, 5, 20))
        assert result.casos_revision_clinica == 2

    def test_counts_comerciales(self, mock_repo, mock_narr):
        repo = MagicMock()
        repo.get_interacciones_del_dia.return_value = [
            _make_interaccion("respondido", comercial=True),
            _make_interaccion("respondido", comercial=False),
        ]
        repo.get_escalamientos_del_dia.return_value = []
        mock_repo.return_value = repo

        result = generate_daily_summary(date(2026, 5, 20))
        assert result.casos_revision_comercial == 1

    def test_counts_escalamientos(self, mock_repo, mock_narr):
        repo = MagicMock()
        repo.get_interacciones_del_dia.return_value = []
        repo.get_escalamientos_del_dia.return_value = [
            _make_escalamiento(),
            _make_escalamiento(),
        ]
        mock_repo.return_value = repo

        result = generate_daily_summary(date(2026, 5, 20))
        assert result.total_escalamientos == 2

    def test_sla_pct_all_cumplidos(self, mock_repo, mock_narr):
        repo = MagicMock()
        repo.get_interacciones_del_dia.return_value = []
        repo.get_escalamientos_del_dia.return_value = [
            _make_escalamiento(cumple_sla=True),
            _make_escalamiento(cumple_sla=True),
        ]
        mock_repo.return_value = repo

        result = generate_daily_summary(date(2026, 5, 20))
        assert result.sla_cumplido_pct == 100.0

    def test_sla_pct_partial(self, mock_repo, mock_narr):
        repo = MagicMock()
        repo.get_interacciones_del_dia.return_value = []
        repo.get_escalamientos_del_dia.return_value = [
            _make_escalamiento(cumple_sla=True),
            _make_escalamiento(cumple_sla=False),
        ]
        mock_repo.return_value = repo

        result = generate_daily_summary(date(2026, 5, 20))
        assert result.sla_cumplido_pct == 50.0

    def test_tiempo_promedio_calculated(self, mock_repo, mock_narr):
        repo = MagicMock()
        repo.get_interacciones_del_dia.return_value = []
        repo.get_escalamientos_del_dia.return_value = [
            _make_escalamiento(tiempo_respuesta=10.0),
            _make_escalamiento(tiempo_respuesta=20.0),
        ]
        mock_repo.return_value = repo

        result = generate_daily_summary(date(2026, 5, 20))
        assert result.tiempo_respuesta_promedio == pytest.approx(15.0, abs=0.1)

    def test_empty_day_returns_zeros(self, mock_repo, mock_narr):
        repo = MagicMock()
        repo.get_interacciones_del_dia.return_value = []
        repo.get_escalamientos_del_dia.return_value = []
        mock_repo.return_value = repo

        result = generate_daily_summary(date(2026, 5, 20))
        assert result.total_interacciones_na == 0
        assert result.total_respondidas == 0
        assert result.sla_cumplido_pct == 0.0
        assert result.tiempo_respuesta_promedio == 0.0

    def test_resumen_id_format(self, mock_repo, mock_narr):
        repo = MagicMock()
        repo.get_interacciones_del_dia.return_value = []
        repo.get_escalamientos_del_dia.return_value = []
        mock_repo.return_value = repo

        result = generate_daily_summary(date(2026, 5, 20))
        assert result.resumen_id == "RES-2026-05-20"

    def test_narrative_included(self, mock_repo, mock_narr):
        repo = MagicMock()
        repo.get_interacciones_del_dia.return_value = []
        repo.get_escalamientos_del_dia.return_value = []
        mock_repo.return_value = repo

        result = generate_daily_summary(date(2026, 5, 20))
        assert result.resumen_narrativo == "Resumen de prueba."

    def test_returns_resumen_diario_instance(self, mock_repo, mock_narr):
        repo = MagicMock()
        repo.get_interacciones_del_dia.return_value = []
        repo.get_escalamientos_del_dia.return_value = []
        mock_repo.return_value = repo

        result = generate_daily_summary(date(2026, 5, 20))
        assert isinstance(result, ResumenDiario)
        assert result.fecha == date(2026, 5, 20)


# ── send_daily_summary ────────────────────────────────────────────────────────

@patch("app.daily_reports._get_repo")
@patch("app.daily_reports.send_message", return_value=True)
class TestSendDailySummary:
    def _make_resumen(self) -> ResumenDiario:
        return ResumenDiario(
            resumen_id="RES-2026-05-20",
            fecha=date(2026, 5, 20),
            total_interacciones_na=10,
            total_respondidas=7,
            total_sin_respuesta=2,
            casos_revision_clinica=1,
            casos_revision_comercial=2,
            total_escalamientos=3,
            sla_cumplido_pct=85.0,
            tiempo_respuesta_promedio=12.5,
            resumen_narrativo="Día activo con 1 alerta clínica.",
        )

    def test_sends_whatsapp_message(self, mock_wa, mock_repo):
        mock_repo.return_value = MagicMock()
        send_daily_summary(self._make_resumen())
        mock_wa.assert_called_once()

    def test_persists_to_repo(self, mock_wa, mock_repo):
        repo = MagicMock()
        mock_repo.return_value = repo
        send_daily_summary(self._make_resumen())
        repo.insert_resumen_diario.assert_called_once()

    def test_message_contains_date(self, mock_wa, mock_repo):
        mock_repo.return_value = MagicMock()
        send_daily_summary(self._make_resumen())
        msg = mock_wa.call_args[0][1]
        assert "20/05/2026" in msg

    def test_message_contains_totals(self, mock_wa, mock_repo):
        mock_repo.return_value = MagicMock()
        send_daily_summary(self._make_resumen())
        msg = mock_wa.call_args[0][1]
        assert "10" in msg  # total_interacciones_na
        assert "7" in msg   # respondidas
        assert "85.0" in msg  # sla_pct

    def test_message_contains_narrative(self, mock_wa, mock_repo):
        mock_repo.return_value = MagicMock()
        send_daily_summary(self._make_resumen())
        msg = mock_wa.call_args[0][1]
        assert "Día activo con 1 alerta clínica." in msg

    def test_whatsapp_error_still_persists(self, mock_wa, mock_repo):
        """Even if WhatsApp fails, the summary is persisted to DB."""
        mock_wa.side_effect = Exception("WA error")
        repo = MagicMock()
        mock_repo.return_value = repo

        send_daily_summary(self._make_resumen())
        repo.insert_resumen_diario.assert_called_once()

    def test_repo_error_does_not_raise(self, mock_wa, mock_repo):
        repo = MagicMock()
        repo.insert_resumen_diario.side_effect = Exception("DB error")
        mock_repo.return_value = repo

        # Must not raise
        send_daily_summary(self._make_resumen())
        mock_wa.assert_called_once()
