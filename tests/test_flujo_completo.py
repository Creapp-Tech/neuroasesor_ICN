"""Integration tests for the core NeurOrientador pipeline.

These tests exercise multiple modules end-to-end without real network calls:
  alarm_filter → (LLM mock) → json_guard → scoring → phase_router → audit_log

All external I/O (LLM, Supabase, WhatsApp) is mocked via unittest.mock.
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from app.alarm_filter import check_alarm
from app.json_guard import parse_and_validate
from app.phase_router import PhaseRouter
from app.scoring import process_f3_scoring
from app.schemas import Paciente


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def router():
    return PhaseRouter()


@pytest.fixture
def paciente_f3_int():
    return Paciente(
        paciente_id="PAC-INT-001",
        telefono="573001234567",
        nombre="Patricia Soto",
        edad=38,
        ciudad="Medellín",
        aseguramiento="Particular",
        consentimiento_datos_clinicos=True,
        consentimiento_teleorientacion=True,
        fase_actual="F3",
        programa_clinico="Cefalea",
    )


# Sample valid LLM JSON output for F3 (Moderado score: D2+D3+D4 = 3+3+2 = 8)
_LLM_RESPONSE_MODERADO = json.dumps({
    "respuesta_visible": "Gracias por tus respuestas. Continuemos con el cuestionario.",
    "notas_internas": "{}",
    "puntaje_dominio": {"D1": 0, "D2": 3, "D3": 3, "D4": 2, "D5": 0, "D6": 0},
    "guia_soporte": "ICHD-3",
    "cie10": "G43",
})

# Sample LLM output triggering Alarma (D1=3 → flag_alarma, score ≥ 13)
_LLM_RESPONSE_ALARMA = json.dumps({
    "respuesta_visible": "Esta situación requiere atención médica urgente.",
    "notas_internas": "{}",
    "puntaje_dominio": {"D1": 3, "D2": 3, "D3": 3, "D4": 3, "D5": 2, "D6": 2},
    "guia_soporte": None,
    "cie10": None,
})


# ── Pipeline sin alarma → F4 ──────────────────────────────────────────────────

def test_flujo_f3_sin_alarma_avanza_a_f4(router, paciente_f3_int):
    """Full pipeline: no alarm keyword → valid JSON → Moderado score → F4."""
    mensaje = "He tenido dolores de cabeza moderados varias veces al mes."

    # 1. Alarm filter — must not detect an alarm
    alarm_detected, _ = check_alarm(mensaje)
    assert alarm_detected is False

    # 2. LLM response (simulated — no real API call)
    raw_response = _LLM_RESPONSE_MODERADO

    # 3. JSON guard — must parse and validate correctly
    response_ia = parse_and_validate(raw_response)
    assert response_ia is not None
    assert response_ia.puntaje_dominio["D2"] == 3

    # 4. Scoring — Moderado (D1=0, D2+D3+D4 = 8, no flag)
    score_result = process_f3_scoring(response_ia.puntaje_dominio)
    assert score_result["flag_alarma"] is False
    assert score_result["score_total"] == 8
    assert score_result["nivel_riesgo"] == "Moderado"
    assert score_result["fase_siguiente"] == "F4"

    # 5. Phase router
    next_phase = router.get_next_phase(paciente_f3_int, response_ia, score_result, False)
    assert next_phase == "F4"


def test_flujo_f3_score_alto_avanza_a_f4(router, paciente_f3_int):
    """Score in Alto range (9-12) also advances to F4."""
    llm_json = json.dumps({
        "respuesta_visible": "...",
        "notas_internas": "{}",
        "puntaje_dominio": {"D1": 0, "D2": 4, "D3": 3, "D4": 3, "D5": 0, "D6": 0},
    })
    response_ia = parse_and_validate(llm_json)
    score_result = process_f3_scoring(response_ia.puntaje_dominio)
    assert score_result["score_total"] == 10
    assert score_result["nivel_riesgo"] == "Alto"

    next_phase = router.get_next_phase(paciente_f3_int, response_ia, score_result, False)
    assert next_phase == "F4"


# ── Pipeline con alarma → HUMANO ──────────────────────────────────────────────

def test_flujo_con_alarma_detectada_en_mensaje(paciente_f3_int):
    """Alarm keyword in message → alarm detected before LLM call."""
    mensaje = "Tengo convulsión ahora mismo, no puedo mover el brazo."

    alarm_detected, keyword = check_alarm(mensaje)
    assert alarm_detected is True
    assert keyword in ("convulsion", "no puedo mover brazo", "no puedo mover")


def test_flujo_score_alarma_va_a_humano(router, paciente_f3_int):
    """D1=3 flag_alarma or score ≥ 13 → Alarma → phase = HUMANO."""
    response_ia = parse_and_validate(_LLM_RESPONSE_ALARMA)
    assert response_ia is not None

    score_result = process_f3_scoring(response_ia.puntaje_dominio)
    assert score_result["flag_alarma"] is True
    assert score_result["nivel_riesgo"] == "Alarma"
    assert score_result["fase_siguiente"] == "HUMANO"

    next_phase = router.get_next_phase(paciente_f3_int, response_ia, score_result, False)
    assert next_phase == "HUMANO"


# ── JSON inválido → HUMANO ────────────────────────────────────────────────────

def test_flujo_json_invalido_va_a_humano(router, paciente_f3_int):
    """LLM returns non-JSON → json_guard returns None → error_json=True → HUMANO."""
    raw_invalid = "Lo siento, no pude procesar tu solicitud en este momento."

    response_ia = parse_and_validate(raw_invalid)
    assert response_ia is None  # json_guard signals failure

    # Caller sets error_json=True when parse returns None
    next_phase = router.get_next_phase(paciente_f3_int, None, None, True)
    assert next_phase == "HUMANO"


def test_flujo_json_campos_faltantes_va_a_humano(router, paciente_f3_int):
    """Partial JSON missing required fields → json_guard returns None → HUMANO."""
    raw_incomplete = '{"respuesta_visible": "Hola"}'

    response_ia = parse_and_validate(raw_incomplete)
    assert response_ia is None

    next_phase = router.get_next_phase(paciente_f3_int, None, None, True)
    assert next_phase == "HUMANO"


# ── Flujo lineal F0 → F1 → F2 → F3 ──────────────────────────────────────────

def test_flujo_lineal_f0_a_f1(router):
    """New patient in F0 advances to F1 on first interaction."""
    paciente = Paciente(paciente_id="PAC-NEW-001", telefono="573009000000", fase_actual="F0")
    result = router.get_next_phase(paciente, None, None, False)
    assert result == "F1"


def test_flujo_lineal_f1_a_f2_con_datos(router):
    """F1 patient with name, age and consent advances to F2."""
    paciente = Paciente(
        paciente_id="PAC-F1-001",
        telefono="573009000001",
        nombre="Laura",
        edad=30,
        consentimiento_datos_clinicos=True,
        fase_actual="F1",
    )
    result = router.get_next_phase(paciente, None, None, False)
    assert result == "F2"


def test_flujo_lineal_f2_a_f3_con_programa(router):
    """F2 patient who selected a clinical program advances to F3."""
    paciente = Paciente(
        paciente_id="PAC-F2-001",
        telefono="573009000002",
        fase_actual="F2",
        programa_clinico="Epilepsia",
    )
    result = router.get_next_phase(paciente, None, None, False)
    assert result == "F3"


# ── Audit log persiste el turno ───────────────────────────────────────────────

@patch("app.audit_log._get_repo")
def test_flujo_guarda_turno_en_supabase(mock_repo, paciente_f3_int):
    """After a conversation turn, audit_log saves it to Supabase."""
    from app.audit_log import log_turno

    repo = MagicMock()
    mock_repo.return_value = repo

    result = log_turno(
        paciente_id=paciente_f3_int.paciente_id,
        telefono=paciente_f3_int.telefono,
        fase="F3",
        mensaje_usuario="Tengo dolor de cabeza moderado.",
        respuesta_agente="Entiendo. ¿Con qué frecuencia ocurre?",
        guia_soporte_turno="ICHD-3",
        tokens_usados=120,
        flag_alarma=False,
        escalado_humano=False,
        version_prompt="v6.0",
    )

    repo.insert_conversacion.assert_called_once()
    assert result.paciente_id == paciente_f3_int.paciente_id
    assert result.fase == "F3"
    assert result.flag_alarma is False


@patch("app.audit_log._get_repo")
def test_flujo_historial_actualizado_correctamente(mock_repo, paciente_f3_int):
    """update_historial appends turn and respects MAX_HISTORIAL_TURNOS cap."""
    from app.audit_log import update_historial
    from app import config

    mock_repo.return_value = MagicMock()

    # Start with empty historial
    assert paciente_f3_int.historial_json == []
    updated = update_historial(paciente_f3_int, "Hola", "Bienvenido")
    assert len(updated) == 2
    assert updated[0] == {"role": "user", "content": "Hola"}
    assert updated[1] == {"role": "assistant", "content": "Bienvenido"}

    # Original must not be mutated
    assert paciente_f3_int.historial_json == []
