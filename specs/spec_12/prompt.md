# Prompt — Spec 12: tests/ Suite de Pruebas Unitarias

Eres un Ingeniero de QA Python con experiencia en sistemas clínicos críticos. Tu tarea es implementar la suite completa de pruebas unitarias requeridas por el documento de criterios de aceptación de NeurOrientador ICN Salud.

## Contexto
El documento (Sección 20) define explícitamente las pruebas requeridas: alarmas, JSON inválido, scoring, transición F3→F4, solicitud de humano, paciente EPS/admin, SLA vencido. Todos los módulos del sistema ya están implementados en specs anteriores. Usa `pytest` + `unittest.mock`.

## Entrega requerida: directorio `tests/`

### `conftest.py` — Fixtures compartidos
```python
@pytest.fixture
def paciente_test() -> Paciente:
    # Paciente con datos mínimos para pruebas
    
@pytest.fixture
def mock_db_repo(mocker):
    # Mock de DBRepository para no llamar a PostgreSQL real
    
@pytest.fixture
def mock_whatsapp(mocker):
    # Mock de whatsapp_client.send_message
```

### `tests/test_alarm_filter.py` (completar los ya existentes)
Casos adicionales obligatorios:
- Mensaje en mayúsculas → detectado
- Mensaje con tildes → detectado
- Mensaje ambiguo sin alarma → no detectado

### `tests/test_scoring.py` (completar)
Todos los casos del documento:
- D1=3 (flag inmediato) → Alarma → HUMANO
- Score=13 sin flag → Alarma → HUMANO
- Score=10 → Alto → F4
- Score=6 → Moderado → F4
- Score=3 → Bajo → F4

### `tests/test_phase_router.py` — NUEVO
```python
def test_f3_alto_va_a_f4()
def test_f3_alarma_va_a_humano()
def test_f0_eps_va_a_admin()
def test_error_json_va_a_humano()
def test_f4_tres_turnos_sin_conversion_va_a_humano()
```

### `tests/test_escalation_sla.py` — NUEVO
```python
def test_sla_cumplido_10_minutos()  # cumple_sla_15min = True
def test_sla_vencido_20_minutos()   # cumple_sla_15min = False, handle_sla_breach llamado
def test_alarma_critica_sla_5_min() # threshold es 5 min, no 15
```

### `tests/test_flujo_eps_admin.py` — NUEVO
```python
def test_paciente_eps_redirige_a_admin()
# Mensaje: "Soy paciente de Sura EPS"
# Esperado: fase = ADMIN, no avanza a F1 clínico
```

### `tests/test_solicitud_humano.py` — NUEVO
```python
def test_solicitud_humano_escala_correctamente()
# Mensaje: "quiero hablar con una persona"
# Esperado: fase = HUMANO, notify_neuroasesor llamado con datos completos
```

### `tests/test_flujo_completo.py` — Integración básica con mocks
```python
def test_flujo_f0_a_f3_sin_alarma()
# Simular: mensaje entrante → alarm_filter pasa → LLM responde JSON → scoring → PostgreSQL actualizado
```

## Reglas de implementación
- Mock todas las llamadas externas: DBRepository, whatsapp_client, LLMClient
- Nunca hacer llamadas reales a APIs en tests
- Cada test debe ser independiente (no depender de estado de otros tests)
- Los tests deben pasar con `pytest tests/ -v` sin necesidad de credenciales reales
