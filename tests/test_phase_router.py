import json
import pytest
from app.phase_router import PhaseRouter
from app.schemas import Paciente, ResponseIA


@pytest.fixture
def router():
    return PhaseRouter()


@pytest.fixture
def basic_paciente():
    return Paciente(
        telefono="573001234567",
        paciente_id="PAC-123",
        fase_actual="F0",
    )


# ── Transiciones desde F3 (scorer) ──────────────────────────────────────────

def test_transition_f3_to_humano_on_alarma(router, basic_paciente):
    basic_paciente.fase_actual = "F3"
    score_result = {"fase_siguiente": "HUMANO", "nivel_riesgo": "Alarma"}
    assert router.get_next_phase(basic_paciente, None, score_result, False) == "HUMANO"


def test_transition_f3_to_f4_on_alto(router, basic_paciente):
    basic_paciente.fase_actual = "F3"
    score_result = {"fase_siguiente": "F4", "nivel_riesgo": "Alto"}
    assert router.get_next_phase(basic_paciente, None, score_result, False) == "F4"


def test_transition_f3_to_f4_on_moderado(router, basic_paciente):
    basic_paciente.fase_actual = "F3"
    score_result = {"fase_siguiente": "F4", "nivel_riesgo": "Moderado"}
    assert router.get_next_phase(basic_paciente, None, score_result, False) == "F4"


# ── Notas internas — JSON ────────────────────────────────────────────────────

def test_transition_on_admin_note_json(router, basic_paciente):
    response_ia = ResponseIA(
        respuesta_visible="...",
        notas_internas=json.dumps({"tipo": "admin"}),
        puntaje_dominio={},
    )
    assert router.get_next_phase(basic_paciente, response_ia, None, False) == "ADMIN"


def test_transition_on_escalamiento_humano_json(router, basic_paciente):
    response_ia = ResponseIA(
        respuesta_visible="...",
        notas_internas=json.dumps({"requiere_escalamiento_humano": True}),
        puntaje_dominio={},
    )
    assert router.get_next_phase(basic_paciente, response_ia, None, False) == "HUMANO"


def test_transition_on_neuroasesor_comercial_json(router, basic_paciente):
    basic_paciente.fase_actual = "F4"
    response_ia = ResponseIA(
        respuesta_visible="...",
        notas_internas=json.dumps({"requiere_neuroasesor_comercial": True}),
        puntaje_dominio={},
    )
    assert router.get_next_phase(basic_paciente, response_ia, None, False) == "HUMANO"


# ── Notas internas — texto libre (fallback) ──────────────────────────────────

def test_transition_on_admin_note_text(router, basic_paciente):
    response_ia = ResponseIA(
        respuesta_visible="...",
        notas_internas="tipo: admin",
        puntaje_dominio={},
    )
    assert router.get_next_phase(basic_paciente, response_ia, None, False) == "ADMIN"


# ── Error JSON ───────────────────────────────────────────────────────────────

def test_transition_on_error_json(router, basic_paciente):
    assert router.get_next_phase(basic_paciente, None, None, True) == "HUMANO"


# ── F4 timeout comercial ─────────────────────────────────────────────────────

def test_transition_f4_timeout_at_3_turns(router, basic_paciente):
    basic_paciente.fase_actual = "F4"
    assert router.get_next_phase(basic_paciente, None, None, False, turno_en_f4=3) == "HUMANO"


def test_transition_f4_no_timeout_at_2_turns(router, basic_paciente):
    basic_paciente.fase_actual = "F4"
    # 2 turnos no son suficientes para escalar
    result = router.get_next_phase(basic_paciente, None, None, False, turno_en_f4=2)
    assert result == "F4"


# ── Flujo lineal normal ──────────────────────────────────────────────────────

def test_f0_advances_to_f1(router, basic_paciente):
    basic_paciente.fase_actual = "F0"
    assert router.get_next_phase(basic_paciente, None, None, False) == "F1"


def test_f1_stays_without_consent(router, basic_paciente):
    basic_paciente.fase_actual = "F1"
    basic_paciente.consentimiento_datos_clinicos = False
    assert router.get_next_phase(basic_paciente, None, None, False) == "F1"


def test_f1_advances_to_f2_when_complete(router, basic_paciente):
    basic_paciente.fase_actual = "F1"
    basic_paciente.nombre = "Ana"
    basic_paciente.edad = 35
    basic_paciente.consentimiento_datos_clinicos = True
    assert router.get_next_phase(basic_paciente, None, None, False) == "F2"


def test_f2_advances_to_f3_with_programa(router, basic_paciente):
    basic_paciente.fase_actual = "F2"
    basic_paciente.programa_clinico = "Cefalea"
    assert router.get_next_phase(basic_paciente, None, None, False) == "F3"


# ── Inyección de datos en prompt ─────────────────────────────────────────────

def test_prompt_injection(router, basic_paciente):
    basic_paciente.nombre = "Juan"
    basic_paciente.fase_actual = "F0"
    prompt = router.get_system_prompt("F0", basic_paciente)
    assert "Juan" in prompt
    assert "F0" in prompt
    assert "NeurOrientador" in prompt
