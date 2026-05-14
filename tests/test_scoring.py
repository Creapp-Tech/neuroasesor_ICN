import pytest
from app.scoring import process_f3_scoring, calculate_score, should_flag_alarm, classify_risk


def test_should_flag_alarm():
    assert should_flag_alarm({"D1": 0}) is False
    assert should_flag_alarm({"D1": 1}) is False
    assert should_flag_alarm({"D1": 2}) is True
    assert should_flag_alarm({"D1": 3}) is True
    assert should_flag_alarm({}) is False


def test_calculate_score():
    assert calculate_score({"D1": 1, "D2": 2, "D3": 3}) == 6
    assert calculate_score({"D1": 3, "D2": 3, "D3": 3, "D4": 3, "D5": 3, "D6": 3}) == 18
    assert calculate_score({}) == 0


def test_classify_risk():
    assert classify_risk(3, False) == "Bajo"
    assert classify_risk(6, False) == "Moderado"
    assert classify_risk(10, False) == "Alto"
    assert classify_risk(14, False) == "Alarma"
    assert classify_risk(5, True) == "Alarma"  # flag toma precedencia


def test_process_f3_scoring_scenarios():
    # D1=3, score=14 → Alarma → HUMANO
    res1 = process_f3_scoring({"D1": 3, "D2": 3, "D3": 3, "D4": 5})
    assert res1["nivel_riesgo"] == "Alarma"
    assert res1["fase_siguiente"] == "HUMANO"

    # D1=2, score=8 → Alarma por flag → HUMANO
    res2 = process_f3_scoring({"D1": 2, "D2": 2, "D3": 2, "D4": 2})
    assert res2["nivel_riesgo"] == "Alarma"
    assert res2["fase_siguiente"] == "HUMANO"

    # D1=0, score=10 → Alto → F4
    res3 = process_f3_scoring({"D2": 5, "D3": 5})
    assert res3["nivel_riesgo"] == "Alto"
    assert res3["fase_siguiente"] == "F4"

    # D1=0, score=6 → Moderado → F4
    res4 = process_f3_scoring({"D2": 3, "D3": 3})
    assert res4["nivel_riesgo"] == "Moderado"
    assert res4["fase_siguiente"] == "F4"

    # D1=0, score=3 → Bajo → F4
    res5 = process_f3_scoring({"D2": 3})
    assert res5["nivel_riesgo"] == "Bajo"
    assert res5["fase_siguiente"] == "F4"

    # puntaje vacío → score=0 → Bajo
    res6 = process_f3_scoring({})
    assert res6["score_total"] == 0
    assert res6["nivel_riesgo"] == "Bajo"
