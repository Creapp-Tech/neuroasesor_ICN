"""Shared fixtures and configuration for the NeurOrientador test suite."""

from unittest.mock import MagicMock

import pytest

from app.schemas import Paciente


@pytest.fixture
def paciente_base() -> Paciente:
    """Minimal patient in F0 — no optional clinical fields filled."""
    return Paciente(
        paciente_id="PAC-TEST-001",
        telefono="573001234567",
        fase_actual="F0",
    )


@pytest.fixture
def paciente_test() -> Paciente:
    """Standard test patient in F3 with full demographics and consent."""
    return Paciente(
        paciente_id="PAC-TEST-001",
        telefono="573001234567",
        nombre="Carlos Gómez",
        edad=35,
        ciudad="Bogotá",
        aseguramiento="Particular",
        consentimiento_datos_clinicos=True,
        consentimiento_teleorientacion=True,
        fase_actual="F3",
        programa_clinico="Cefalea",
    )


@pytest.fixture
def paciente_f3() -> Paciente:
    """Patient ready for F3 scoring — consent given, demographics known."""
    return Paciente(
        paciente_id="PAC-TEST-002",
        telefono="573009876543",
        nombre="Ana Torres",
        edad=42,
        ciudad="Bogotá",
        aseguramiento="Particular",
        consentimiento_datos_clinicos=True,
        consentimiento_teleorientacion=True,
        fase_actual="F3",
        programa_clinico="Cefalea",
        nivel_riesgo="Alto",
        score_total=10,
    )


@pytest.fixture
def mock_db_repo() -> MagicMock:
    """Pre-configured MagicMock for SupabaseRepository — no real DB calls."""
    repo = MagicMock()
    repo.get_paciente_by_telefono.return_value = None
    repo.get_conversaciones_by_paciente_id.return_value = []
    repo.get_escalamientos_sin_respuesta.return_value = []
    return repo


@pytest.fixture
def mock_whatsapp() -> MagicMock:
    """MagicMock for whatsapp_client.send_message — always succeeds."""
    return MagicMock(return_value=True)
