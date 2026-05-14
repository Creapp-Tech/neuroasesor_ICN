import pytest
from app.alarm_filter import check_alarm, normalize_text


def test_normalize_text():
    assert normalize_text("HOLA mundo") == "hola mundo"
    assert normalize_text("¿Convulsión?") == "convulsion"
    assert normalize_text("Pérdida de conciencia") == "perdida de conciencia"
    assert normalize_text("fiebre + cuello") == "fiebre + cuello"


def test_check_alarm_positive():
    assert check_alarm("me esta dando una convulsion")[0] is True
    assert check_alarm("tengo el peor dolor de mi vida")[0] is True
    assert check_alarm("pense en hacerme daño")[0] is True
    assert check_alarm("siento vision doble subita")[0] is True
    assert check_alarm("tengo rigidez de nuca")[0] is True


def test_check_alarm_accents():
    assert check_alarm("convulsión")[0] is True
    assert check_alarm("convulsion")[0] is True
    assert check_alarm("PÉRDIDA DE CONCIENCIA")[0] is True
    assert check_alarm("visión doble súbita")[0] is True


def test_check_alarm_negative():
    assert check_alarm("hola como estas")[0] is False
    assert check_alarm("me duele la cabeza un poco")[0] is False
    assert check_alarm("quisiera agendar una cita")[0] is False
    assert check_alarm("tengo migraña desde hace años")[0] is False
    assert check_alarm("el niño tiene gripa")[0] is False


def test_check_alarm_empty():
    assert check_alarm("")[0] is False
    assert check_alarm(None)[0] is False
