import pytest
from app.json_guard import parse_and_validate
from app.schemas import ResponseIA


def test_parse_valid_json_full():
    raw = """
    {
        "respuesta_visible": "Hola paciente",
        "notas_internas": "Todo ok",
        "puntaje_dominio": {"D1": 1, "D2": 0, "D3": 0, "D4": 0, "D5": 0, "D6": 0},
        "guia_soporte": "ICHD-3",
        "cie10": "G43"
    }
    """
    result = parse_and_validate(raw)
    assert isinstance(result, ResponseIA)
    assert result.respuesta_visible == "Hola paciente"
    assert result.puntaje_dominio["D1"] == 1


def test_parse_valid_json_minimal():
    raw = """
    {
        "respuesta_visible": "Hola",
        "notas_internas": "N/A",
        "puntaje_dominio": {"D1": 0, "D2": 0, "D3": 0, "D4": 0, "D5": 0, "D6": 0}
    }
    """
    result = parse_and_validate(raw)
    assert isinstance(result, ResponseIA)
    assert result.guia_soporte is None
    assert result.cie10 is None


def test_parse_json_with_surrounding_text():
    raw = """
    Claro, aquí tienes la respuesta:
    ```json
    {
        "respuesta_visible": "Texto con ruido",
        "notas_internas": "notas",
        "puntaje_dominio": {"D1": 0, "D2": 0, "D3": 0, "D4": 0, "D5": 0, "D6": 0}
    }
    ```
    Espero que te sirva.
    """
    result = parse_and_validate(raw)
    assert isinstance(result, ResponseIA)
    assert result.respuesta_visible == "Texto con ruido"


def test_parse_invalid_json():
    assert parse_and_validate("No soy un json") is None
    assert parse_and_validate("") is None
    assert parse_and_validate('{"key": "missing"}') is None  # faltan campos obligatorios


def test_parse_broken_json():
    raw = '{ "respuesta_visible": "incompleto...'  # sin cerrar
    assert parse_and_validate(raw) is None
