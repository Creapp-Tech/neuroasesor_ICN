"""Tests for the EPS / administrative patient flow.

When the LLM detects an EPS or administrative query, it sets
notas_internas with tipo=admin. The PhaseRouter must redirect to ADMIN
and never advance to F1 clinical.
"""

import json

import pytest

from app.phase_router import PhaseRouter
from app.schemas import Paciente, ResponseIA


@pytest.fixture
def router():
    return PhaseRouter()


@pytest.fixture
def paciente_eps():
    return Paciente(
        paciente_id="PAC-EPS-001",
        telefono="573001234567",
        nombre="Luis Martínez",
        edad=45,
        aseguramiento="Sanitas EPS",
        fase_actual="F0",
    )


class TestFlujoEpsAdmin:
    def test_paciente_eps_redirige_a_admin(self, router, paciente_eps):
        """LLM notas_internas tipo=admin → phase = ADMIN, not F1 clinical."""
        response_ia = ResponseIA(
            respuesta_visible="Le redirigimos al canal administrativo de ICN Salud.",
            notas_internas=json.dumps({"tipo": "admin"}),
            puntaje_dominio={},
        )
        result = router.get_next_phase(paciente_eps, response_ia, None, False)
        assert result == "ADMIN"

    def test_notas_admin_texto_libre(self, router, paciente_eps):
        """Text-based fallback 'tipo: admin' also triggers ADMIN redirect."""
        response_ia = ResponseIA(
            respuesta_visible="...",
            notas_internas="tipo: admin",
            puntaje_dominio={},
        )
        result = router.get_next_phase(paciente_eps, response_ia, None, False)
        assert result == "ADMIN"

    def test_notas_admin_json_tipo_igual_admin(self, router, paciente_eps):
        """JSON with tipo=admin string value is recognised correctly."""
        response_ia = ResponseIA(
            respuesta_visible="Canal administrativo.",
            notas_internas='{"tipo": "admin", "motivo": "consulta_eps"}',
            puntaje_dominio={},
        )
        result = router.get_next_phase(paciente_eps, response_ia, None, False)
        assert result == "ADMIN"

    def test_fase_admin_no_avanza_automaticamente(self, router, paciente_eps):
        """Once in ADMIN, the patient stays there (no automatic linear advance)."""
        paciente_eps.fase_actual = "ADMIN"
        result = router.get_next_phase(paciente_eps, None, None, False)
        assert result == "ADMIN"

    def test_f0_sin_senal_eps_avanza_a_f1(self, router, paciente_eps):
        """Without an admin signal, F0 normally advances to F1."""
        response_ia = ResponseIA(
            respuesta_visible="Bienvenido al NeurOrientador.",
            notas_internas=json.dumps({}),
            puntaje_dominio={},
        )
        result = router.get_next_phase(paciente_eps, response_ia, None, False)
        assert result == "F1"

    def test_f0_sin_response_ia_avanza_a_f1(self, router, paciente_eps):
        """F0 with no LLM response also advances to F1 (linear default)."""
        result = router.get_next_phase(paciente_eps, None, None, False)
        assert result == "F1"

    def test_admin_tiene_prioridad_sobre_flujo_lineal(self, router, paciente_eps):
        """Admin signal takes precedence over the normal F0→F1 linear flow."""
        response_ia = ResponseIA(
            respuesta_visible="Autorización EPS requerida.",
            notas_internas=json.dumps({"tipo": "admin"}),
            puntaje_dominio={},
        )
        result = router.get_next_phase(paciente_eps, response_ia, None, False)
        assert result == "ADMIN"
        assert result != "F1"
