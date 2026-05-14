# Prompt — Spec 6: phase_router.py + prompts/

Eres un Ingeniero de Software Python especializado en agentes conversacionales clínicos. Tu tarea es implementar el enrutador de fases y los prompts versionados del sistema NeurOrientador de ICN Salud.

## Contexto
El sistema tiene 7 fases en el MVP: F0, F1, F2, F3, F4, ADMIN, HUMANO. Cada una tiene su prompt y reglas de transición. La lógica de transición de fases es responsabilidad del backend Python, no del modelo de IA. Los specs anteriores (config, schemas, scoring) ya están implementados.

## Entrega requerida

### Parte 1: Directorio `prompts/`
Crea los siguientes archivos de texto con el contenido de cada prompt según el documento V6/V5:

**`prompts/base_v6.txt`** — Incluir:
- Rol del sistema: "Eres NeurOrientador, el sistema de teleorientación neurológica de ICN Salud."
- Tríada de tono obligatoria: Clínico + Humano + Comercial (definición de cada uno)
- Reglas absolutas: JSON siempre, nunca diagnóstico, nunca medicamentos, siempre teleorientación no consulta, F3 obligatoria
- Lenguaje prohibido vs obligatorio (tabla del documento)
- Placeholders: {{nombre}}, {{edad}}, {{ciudad}}, {{aseguramiento}}, {{fase_actual}}, {{programa_clinico}}, {{nivel_riesgo}}

**`prompts/f0_v6.txt`** — Clasificar intención del primer mensaje:
- Síntomas/interés clínico/precio/cita → tipo=teleorientacion
- EPS/admin → tipo=admin (incluir link icnsalud.com/#contacto)
- Particular/prepagada → tipo=teleorientacion
- Mensaje inicial de bienvenida según copia de referencia del documento

**`prompts/f1_v6.txt`** — Consentimiento e identificación:
- Tres puntos de consentimiento (Ley 1581/2012, naturaleza teleorientación, disponibilidad 24/7)
- Capturar nombre, edad, ciudad, aseguramiento (máx 2 preguntas por turno)
- Si EPS detectado → notas_internas: tipo=admin
- Si datos completos → mostrar programas disponibles

**`prompts/f2_v6.txt`** — Selección de problema neurológico:
- 10 problemas disponibles (lista exacta del documento)
- Regla: un problema por teleconsulta
- Si pide precio/cita → explicar que F3 es primero
- Si detecta señal emocional fuerte → requiere_escalamiento_humano=TRUE

**`prompts/f3_v6.txt`** — Teleorientación clínica (ejemplo Cefalea/ICHD-3):
- 6 dominios D1-D6 con preguntas de referencia y tabla de scoring
- Cierre anticipado permitido si ya hay suficiente orientación clínica
- Lenguaje obligatorio de teleorientación
- Adaptar guía según programa_clinico activo

**`prompts/f4_v6.txt`** — Conversión:
- Estructura T1 (resultado), T2 (consecuencia), T3 (propuesta), T4 (cierre con horarios concretos)
- Manejo de objeciones: precio, "ya fui al médico", miedo, "quiero pensarlo", EPS
- Nunca preguntar "¿quieres agendar?" — usar opciones concretas de horario
- Si duda repetida 3+ turnos → requiere_neuroasesor_comercial=TRUE

**`prompts/admin_v6.txt`** y **`prompts/humano_v6.txt`** — Mensajes de redirección y espera.

### Parte 2: `phase_router.py`

```python
class PhaseRouter:
    def get_system_prompt(self, fase: str, paciente: Paciente) -> str:
        """
        Carga prompt de la fase e inyecta datos del paciente.
        Siempre incluye el prompt base + el prompt de fase específica.
        """
    
    def get_next_phase(
        self,
        paciente: Paciente,
        response_ia: Optional[ResponseIA],
        score_result: Optional[dict],  # output de process_f3_scoring
        error_json: bool,
        turno_en_f4: int  # contador de turnos en F4
    ) -> str:
        """
        Determina la siguiente fase. Lógica backend, no depende del modelo.
        
        Reglas (en orden de prioridad):
        1. error_json persistente → "HUMANO"
        2. score_result presente (F3 completada): usar classify_risk
        3. notas_internas contiene tipo=admin → "ADMIN"
        4. notas_internas contiene requiere_escalamiento_humano=TRUE → "HUMANO"
        5. notas_internas contiene requiere_neuroasesor_comercial=TRUE → "HUMANO"
        6. turno_en_f4 >= 3 sin conversion → "HUMANO"
        7. Default: mantener fase actual o avanzar según flujo normal
        """
```

## Reglas de transición de fases (backend, no modelo)
- F0 → F1 (teleorientacion) o ADMIN (EPS/admin)
- F1 → F2 (cuando consentimiento y datos completos)
- F2 → F3 (siempre, incluso si pide precio/cita)
- F3 → F4 (Bajo/Moderado/Alto) o HUMANO (Alarma)
- F4 → HUMANO (si escala comercial o pide humano)
- ADMIN → fin de flujo agente
- HUMANO → fin de flujo agente

## Pruebas: `tests/test_phase_router.py`
- F3 con nivel_riesgo=Alto → F4
- F3 con flag_alarma=True → HUMANO
- F0 con tipo=admin en notas → ADMIN
- error_json=True → HUMANO
- F4 turno 3 sin conversión → HUMANO
