"""Unit tests for escalation_service.

Cubre los tres casos descritos en la spec:
1. Respuesta en 10 min → cumple SLA.
2. Respuesta en 20 min → SLA incumplido y se llama a handle_sla_breach.
3. Alarma crítica con tiempo > 5 min → SLA crítico incumplido.
"""

import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
import pytz

# Import the module under test
from app.escalation_service import (
    Escalamiento,
    check_sla_compliance,
    handle_sla_breach,
    register_human_response,
    trigger_alarm_escalamiento,
)

# Simple dummy patient compatible with the functions (only needed attributes)
class DummyPatient:
    def __init__(self):
        self.paciente_id = "PAC-001"
        self.telefono = "+573001234567"
        self.nombre = "Juan Perez"
        self.nivel_riesgo = "alto"
        self.fase_actual = "F2"

# Helper to create an Escalamiento instance without persisting to DB
def make_escalamiento(tipo: str, minutos_respuesta: float | None = None) -> Escalamiento:
    esc = Escalamiento(
        escalamiento_id="ESC-TEST",
        paciente_id="PAC-001",
        tipo=tipo,
        motivo="motivo de prueba",
        fase_origen="F2",
        timestamp_escalamiento=datetime.now(pytz.utc),
    )
    if minutos_respuesta is not None:
        esc.tiempo_respuesta_humano = minutos_respuesta
    return esc

def test_check_sla_compliance_success():
    """Respuesta en 10 min (tipo genérico) debe cumplir SLA de 15 min."""
    esc = make_escalamiento(tipo="clinico", minutos_respuesta=10)
    assert check_sla_compliance(esc) is True
    assert esc.cumple_sla_15min is True

def test_check_sla_compliance_failure_calls_handle():
    """Respuesta en 20 min (tipo genérico) supera los 15 min y debe invocar handle_sla_breach."""
    esc = make_escalamiento(tipo="clinico", minutos_respuesta=20)
    with patch("app.escalation_service.handle_sla_breach") as mock_handle:
        result = check_sla_compliance(esc)
        assert result is False
        assert esc.cumple_sla_15min is False
        mock_handle.assert_called_once_with(esc)

def test_check_sla_compliance_critical_alarm():
    """Alarma crítica tiene umbral de 5 min; 6 min debe fallar y llamar a handle_sla_breach."""
    esc = make_escalamiento(tipo="alarma_critica", minutos_respuesta=6)
    with patch("app.escalation_service.handle_sla_breach") as mock_handle:
        result = check_sla_compliance(esc)
        assert result is False
        assert esc.cumple_sla_15min is False
        mock_handle.assert_called_once_with(esc)

# ---------------------------------------------------------------------------
# Tests for the high‑level flow `trigger_alarm_escalamiento`.
# ---------------------------------------------------------------------------

@patch("app.escalation_service.whatsapp_send")
@patch("app.escalation_service.notify_neuroasesor")
def test_trigger_alarm_escalamiento(mock_notify, mock_whatsapp):
    """Verifica que se envía el mensaje al paciente y se crea el escalamiento."""
    patient = DummyPatient()
    # Llamar al flujo completo
    esc = trigger_alarm_escalamiento(patient, motivo_alarma="convulsion", notas="nota clínica")
    # Se debe haber llamado a whatsapp_send con el mensaje de urgencia
    assert mock_whatsapp.called
    # Se debe haber notificado al neuroasesor
    mock_notify.assert_called_once()
    # El escalamiento resultante debe tener tipo alarma_critica
    assert esc.tipo == "alarma_critica"
    assert esc.paciente_id == patient.paciente_id

# ---------------------------------------------------------------------------
# Test for `register_human_response` – se mockea la dependencia a la base de datos.
# ---------------------------------------------------------------------------

@patch("app.escalation_service.check_sla_compliance", return_value=True)
@patch("app.escalation_service.SessionLocal")
def test_register_human_response(mock_session_factory, mock_check):
    """Simula la actualización de la respuesta humana y verifica cálculo de minutos."""
    # Simular sesión DB que devuelve el escalamiento
    class DummySession:
        def __init__(self):
            self._escalamiento = None
        def query(self, model):
            class Query:
                def __init__(self, outer):
                    self.outer = outer
                def filter_by(self, **kwargs):
                    return self
                def first(self):
                    return self.outer._escalamiento
            return Query(self)
        def add(self, obj):
            self._escalamiento = obj
        def commit(self):
            pass
        def refresh(self, obj):
            pass
        def close(self):
            pass
    dummy_session = DummySession()
    mock_session_factory.return_value = dummy_session

    # Creamos un escalamiento base y lo asignamos a la sesión mockeada
    base_esc = make_escalamiento(tipo="clinico")
    dummy_session._escalamiento = base_esc

    # Ejecutar la función
    minutos = register_human_response(base_esc.escalamiento_id)
    # Debería devolver un número positivo de minutos
    assert isinstance(minutos, float)
    assert minutos >= 0
    # La función debe haber llamado a check_sla_compliance
    mock_check.assert_called_once()

