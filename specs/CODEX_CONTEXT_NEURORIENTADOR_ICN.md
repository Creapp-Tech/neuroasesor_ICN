# CONTEXTO MAESTRO PARA CLAUDE CODE — NeurOrientador + NeuroAsistente ICN Salud

> Objetivo del archivo: entregar a CLAUDE CODE una fuente única, explícita y completa para implementar el agente en Python sin inventar reglas, campos, fases, mensajes, flujos, escalamiento ni lógica clínica/comercial.  
> Regla de uso: cuando exista conflicto entre versiones, usar V6 como autoridad vigente. V5, V4.1, V3, V2 y V1 quedan como respaldo histórico y fuente de detalles si no contradicen V6.

---

## 0. Instrucciones obligatorias para CLAUDE CODE

1. No inventar funcionalidades, fases, campos, umbrales, rutas, mensajes, prompts, integraciones ni nombres de hojas.
2. Implementar primero el MVP vigente descrito en V6.
3. Tratar V6 como la versión canónica. V5 y anteriores solo complementan cuando V6 no define un detalle.
4. Toda salida del agente de IA debe ser JSON válido en la estructura establecida.
5. La lógica crítica NO debe quedar únicamente en prompts. Debe implementarse en backend Python/Make-equivalente:
   - filtro de alarmas antes de llamar al modelo,
   - validación JSON,
   - reintentos de JSON,
   - cálculo de score_total,
   - clasificación de nivel_riesgo,
   - transición de fases,
   - activación de flag_alarma,
   - registro de trazabilidad,
   - escalamiento humano,
   - SLA de respuesta humana.
6. El agente nunca debe diagnosticar, formular medicamentos ni indicar dosis.
7. El servicio siempre debe llamarse teleorientación, no consulta médica.
8. Todo paciente debe completar F3 antes de agendar, incluso si pregunta por precio o cita.
9. Una teleconsulta equivale a un solo problema neurológico. Si hay múltiples problemas, se agenda una teleconsulta separada por cada uno.
10. Todo escalamiento debe contener datos completos para el Neuroasesor.
11. Todo lo que haga el NeuroAsistente y el Neuroasesor debe quedar registrado.
12. Todo mensaje debe mantener la tríada de tono: clínico + humano + comercial.
13. CLAUDE CODE debe pedir o marcar como variable de entorno cualquier secreto: tokens de WhatsApp, ManyChat, Make, Gemini/OpenAI, Google, Zoho o webhooks. Nunca hardcodear secretos.

---

## 1. Autoridad de versiones y resolución de conflictos

Orden de autoridad:

1. V6.0 — fuente vigente. Incluye WhatsApp + ManyChat, Make AI Agents, Gemini, Google Sheets, SLA 15 min, supervisión diaria y trazabilidad humana.
2. V5.0 — base operativa final previa. Conserva reglas de disponibilidad 24/7, tono triádico, F3 obligatoria, F4 conversión explícita y NeuroAsistente.
3. V4.1 — MVP + NeuroAsistente con trazabilidad automática.
4. V3.0 — versión ampliada con F2.5 y componentes psicosociales. Usar solo si se decide fase posterior; no imponer en MVP V6 si está pospuesto o simplificado.
5. V2.0 — base legal/metodológica, consentimiento y guías clínicas.
6. V1.0 — arquitectura inicial histórica.

Regla: si V6 contradice versiones anteriores, gana V6.

---

## 2. Producto a implementar

Sistema clínico-comercial de teleorientación neurológica de ICN Salud compuesto por:

- NeurOrientador: flujo F0–F4 para recibir pacientes, orientar, clasificar riesgo y convertir a cita.
- NeuroAsistente: acompañamiento posterior a la agenda, confirmación, preparación, recordatorios, seguimiento y retroalimentación.
- Neuroasesor: operador humano que responde escalamientos, supervisa el NeuroAsistente, valida calidad, detecta oportunidades y reporta gestión diaria.

Objetivo del MVP: recibir pacientes, realizar teleorientación, clasificar riesgo, generar confianza, convertir a cita y acompañar antes/después de la consulta.

---

## 3. Stack tecnológico vigente V6

- Canal principal: WhatsApp Business API.
- Canal complementario/panel operativo MVP: ManyChat.
- Orquestación: Make con AI Agents.
- Modelo IA en V6: Gemini.
- Persistencia operativa: Google Sheets.
- Gestión operativa inicial: ManyChat como CRM ligero.
- CRM futuro evaluado: Zoho CRM.

Nota histórica: versiones anteriores mencionan ChatGPT API/GPT-4o. Para V6, usar Gemini si se sigue la especificación vigente. Si el equipo decide usar OpenAI en Python, mantener exactamente las mismas estructuras, validaciones y reglas.

---

## 4. Canales y flujo integrado V6

Canales de entrada:

- WhatsApp Business API: conversación clínica principal 24/7, webhook permanente, lógica F0–F4 y NeuroAsistente.
- ManyChat: entrada complementaria y panel operativo del Neuroasesor; preclasifica intención admin/clínico; actúa como CRM ligero en MVP.

Flujo integrado:

1. Paciente escribe por WhatsApp o ManyChat.
2. ManyChat detecta primer contacto o paciente existente y puede aplicar filtro de intención.
3. ManyChat dispara webhook de Make con parámetros del mensaje.
4. Make ejecuta filtro de alarma, AI Agent, lógica backend y actualización de Sheets.
5. Make envía respuesta_visible por WhatsApp; ManyChat actualiza estado del contacto.
6. Si hay escalamiento, Make notifica al Neuroasesor; ManyChat asigna la conversación y registra prioridad.

---

## 5. Principios legales y clínicos obligatorios

- NeurOrientador es teleorientación en salud neurológica.
- No es consulta médica.
- No emite diagnósticos clínicos.
- No formula medicamentos.
- No recomienda dosis.
- Resultado: clasificación/evaluación de riesgo, no diagnóstico.
- Lenguaje obligatorio:
  - “Esto sugiere un nivel de riesgo…”
  - “El especialista podrá confirmar…”
  - “Tu evaluación de riesgo está completa. Este resultado no es un diagnóstico médico.”
- Lenguaje prohibido:
  - “Tienes migraña”
  - “Eso es epilepsia”
  - “Tu diagnóstico es…”
  - “Debes tomar este medicamento”
  - “Soy tu médico virtual”

Base metodológica:

- ICHD-3.
- DSM-5-TR.
- Guías ICN.
- Modelo UNI de Evaluación de Riesgo en Salud.
- Guías por programa según las tablas de las fuentes completas incluidas más abajo.

---

## 6. Fases MVP vigentes

Fases incluidas:

- F0: clasificación inicial de intención.
- F1: consentimiento e identificación del paciente.
- F2: selección de problema neurológico.
- F3: teleorientación clínica estructurada y scoring.
- F4: conversión a cita.
- NeuroAsistente: acompañamiento formal post-agenda.

Fases pospuestas o no centrales en MVP V6 según versiones previas:

- F5 seguimiento automático avanzado de citas, si no está absorbido por NeuroAsistente.
- F6 educación preventiva recurrente.
- ESRI.
- Investigación avanzada.
- Cohortes complejas.
- Modelos predictivos.

Regla no negociable: F3 siempre antes de agenda.

---

## 7. Tono obligatorio

Todo mensaje debe integrar simultáneamente:

- Clínico: confianza, seriedad, rigor.
- Humano: cercanía, calidez, validación emocional.
- Comercial: orientar hacia la acción sin presión agresiva.

Aplicación:

- F3: lidera lo clínico, siempre con validación emocional.
- F4: cierre comercial explícito basado en hallazgos reales; ofrecer horarios concretos, no preguntas abiertas.
- NeuroAsistente: lidera lo humano, mantiene credibilidad clínica y facilita continuidad.

---

## 8. Filtro de alarmas antes del modelo

Debe ejecutarse antes de cualquier llamada a IA. Si detecta alarma:

1. No llamar al modelo.
2. Activar flag_alarma = TRUE.
3. Notificar Neuroasesor/ICN de inmediato.
4. Enviar al paciente orientación a urgencias + datos de contacto ICN.
5. Registrar motivo_escalamiento.

Palabras/frases mínimas de alarma:

- convulsión / convulsiones
- pérdida de conciencia / desmayo
- no puedo mover brazo/pierna/cara
- peor dolor de mi vida
- dolor de inicio súbito
- rigidez de nuca
- fiebre + cuello
- pensamiento suicida
- hacerme daño
- cefalea en trueno
- visión doble súbita
- no puedo hablar de repente
- convulsión activa
- ACV probable

Alarmas clínicas críticas tienen objetivo de respuesta humana inmediata menor a 5 minutos.

---

## 9. JSON obligatorio del agente IA

Estructura base V6/V5:

```json
{
  "respuesta_visible": "Texto al paciente por WhatsApp",
  "notas_internas": "Solo visible para equipo ICN",
  "puntaje_dominio": {"D1": 0, "D2": 0, "D3": 0, "D4": 0, "D5": 0, "D6": 0},
  "guia_soporte": "ICHD-3 criterio X / DSM-5-TR criterio Y / Guía ICN",
  "cie10": "G43.009"
}
```

Reglas:

- nivel_riesgo, score_total, flag_alarma y fase_siguiente los calcula backend, no el modelo.
- El modelo puede sugerir señales en notas_internas, pero backend decide.
- La respuesta debe ser JSON puro, sin texto fuera del objeto.
- Si JSON inválido: reintentar máximo 2 veces con instrucción “Responde SOLO JSON válido”. Si persiste en tercer fallo, escalar a HUMANO.

---

## 10. Backend Python/Make-equivalente requerido

Módulos recomendados en Python:

- `config.py`: variables de entorno, modelos, tokens, URLs, timezone Colombia.
- `schemas.py`: Pydantic/dataclasses para Paciente, Conversacion, Cita, Escalamiento, Interacciones.
- `alarm_filter.py`: detección previa de alarmas.
- `prompts/`: prompts versionados por fase.
- `llm_client.py`: cliente Gemini/OpenAI con salida JSON.
- `json_guard.py`: parseo, validación y reintentos.
- `scoring.py`: suma D1–D6, umbrales, riesgo, flags.
- `phase_router.py`: transición de fases.
- `sheets_repository.py`: lectura/escritura Google Sheets.
- `manychat_client.py`: estados, etiquetas, asignación humano.
- `whatsapp_client.py`: envío/recepción WhatsApp.
- `escalation_service.py`: notificación al Neuroasesor y SLA.
- `neuroasistente_service.py`: mensajes automáticos, seguimiento y resumen diario.
- `neuroasesor_service.py`: registro de intervenciones humanas.
- `daily_reports.py`: resumen diario NeuroAsistente y reporte diario Neuroasesor.
- `audit_log.py`: trazabilidad completa.
- `tests/`: pruebas unitarias para alarmas, JSON, scoring, fases y SLA.

---

## 11. Google Sheets — entidades mínimas V6

Hojas obligatorias:

- PACIENTES.
- CONVERSACIONES.
- CITAS, si se agenda en MVP o se sincroniza con agenda.
- ESCALAMIENTOS.
- NEUROASISTENTE_INTERACCIONES.
- NEUROASESOR_INTERACCIONES.
- RESUMENES_DIARIOS.
- Opcional/según consentimiento: COHORTES_INVESTIGACION.

Campos exactos y ampliados están en las fuentes completas anexas. CLAUDE CODE debe usarlos como referencia para crear modelos y migraciones.

---

## 12. SLA de respuesta humana V6

KPI obligatorio:

- Neuroasesor debe responder cualquier caso escalado en máximo 15 minutos.
- Alarmas críticas: objetivo inmediato menor a 5 minutos.

Campos obligatorios:

- timestamp_escalamiento.
- timestamp_respuesta_humano.
- tiempo_respuesta_humano.
- cumple_sla_15min.
- tipo_escalamiento: Clínico / Comercial / Solicitud_paciente / Error_sistema / Alarma_critica.
- prioridad_sla: Alta / Media / Normal.

Si incumple SLA:

- Registrar incumplimiento en ESCALAMIENTOS.
- Alertar coordinador ICN.
- Marcar conversación como vencida en ManyChat.
- Registrar incidencia en resumen diario.
- Acumular para métricas semanales.

---

## 13. Priorización operativa V6

Orden obligatorio:

1. Pacientes ya agendados con ICN Salud: máxima prioridad.
2. Pacientes particulares: segunda prioridad.
3. Otros pacientes: tercera prioridad.

Aplicar en SLA, escalamiento, NeuroAsistente, cola de seguimiento y asignación de agenda.

---

## 14. Escalamiento humano

Todo escalamiento debe enviar:

- nombre completo,
- teléfono,
- problema principal,
- nivel de riesgo,
- resumen clínico,
- motivo del escalamiento,
- prioridad del paciente,
- fase en que ocurrió.

Tipos y objetivos:

- Alarma clínica crítica: menor a 5 minutos + urgencias + Neuroasesor.
- Escalamiento clínico: menor o igual 15 minutos.
- Escalamiento comercial: menor o igual 15 minutos.
- Solicitud del paciente: menor o igual 15 minutos.
- Error del sistema: menor o igual 15 minutos.
- Señal clínica en NeuroAsistente: menor o igual 15 minutos.
- Señal comercial en NeuroAsistente: menor o igual 30 minutos.

---

## 15. NeuroAsistente

No es autónomo sin supervisión. Debe ser supervisado diariamente por Neuroasesor.

Debe registrar cada interacción en NEUROASISTENTE_INTERACCIONES y producir al final del día un resumen con:

- pacientes contactados,
- mensajes enviados,
- respuestas del paciente,
- casos con revisión clínica,
- casos con revisión comercial,
- sin respuesta tras 24h,
- métricas del día.

Horario de resumen por defecto: 8:00 PM hora Colombia, lunes a sábado.

---

## 16. Neuroasesor

Responsabilidades:

- responder escalamientos dentro del SLA,
- supervisar NeuroAsistente,
- auditar calidad de respuestas,
- detectar oportunidades comerciales,
- detectar problemas clínicos no resueltos,
- generar reporte diario.

Toda intervención directa debe registrarse en NEUROASESOR_INTERACCIONES.

Campos mínimos según V6:

- neuroasesor_interaccion_id,
- paciente_id,
- fecha_hora_inicio,
- fecha_hora_fin,
- tiempo_respuesta_humano,
- cumple_sla_15min,
- canal,
- tipo_interaccion,
- prioridad_paciente,
- resumen_conversacion,
- resultado,
- oportunidad_detectada,
- incidencia,
- notas_internas,
- responsable,
- version_flujo.

---

## 17. Reportes diarios

Resumen diario NeuroAsistente: generado por sistema.

Reporte diario Neuroasesor: completado por el Neuroasesor con:

- con quién habló,
- temas tratados,
- casos cerrados,
- casos abiertos,
- pacientes que requieren seguimiento,
- incidencias relevantes,
- oportunidades detectadas.

---

## 18. F4 conversión

Reglas:

- Orientar a cierre.
- Ofrecer horarios concretos.
- No preguntar “¿Quieres agendar?”
- Usar “¿Te queda mejor el jueves en la mañana o el viernes en la tarde?”
- Validar objeciones sin presión agresiva.
- Si pide humano, escalar.
- EPS/admin se redirige a `https://icnsalud.com/#contacto`.

---

## 19. Mensajes de referencia

Mensaje inicial F0:

“Hola, bienvenido/a a ICN Salud 👋 Soy NeurOrientador, el sistema de orientación neurológica de ICN Salud. Estoy aquí para ayudarte a entender mejor lo que está pasando y orientarte hacia el paso más adecuado. ¿En qué te puedo ayudar hoy?”

Consentimiento F1 resumido V5/V6:

“Antes de comenzar, necesito contarte tres cosas importantes:
1. Tus datos están protegidos. Toda la información que compartas es confidencial y se trata según la Ley 1581 de 2012.
2. Esto es una teleorientación, no una consulta médica. Lo que obtendrás es una evaluación de riesgo — no un diagnóstico. El especialista es quien confirma.
3. Puedes usar este canal cuando necesites. Estamos disponibles las 24 horas, los 7 días de la semana.
¿Aceptas estos términos para continuar? Responde SÍ o NO.”

---

## 20. Criterios de aceptación para implementación Python

La implementación se considera aceptable si:

- Recibe mensajes WhatsApp/ManyChat vía webhook.
- Identifica o crea paciente.
- Ejecuta filtro de alarmas antes del modelo.
- Selecciona prompt por fase.
- Llama al modelo con historial acotado.
- Valida JSON estricto.
- Reintenta JSON inválido y escala si persiste.
- Calcula score_total, nivel_riesgo y flag_alarma fuera del modelo.
- Registra cada turno en CONVERSACIONES.
- Actualiza PACIENTES.
- Mantiene historial_json truncado.
- Ejecuta F0–F4 con F3 obligatoria.
- Genera reporte de riesgo al cierre de F3.
- Maneja F4 con conversión explícita.
- Registra y mide SLA de escalamientos.
- Registra interacciones NeuroAsistente y Neuroasesor.
- Genera resumen diario.
- Tiene pruebas unitarias para: alarmas, JSON inválido, scoring, transición F3→F4, solicitud de humano, paciente EPS/admin, SLA vencido.

---

## 21. Fuentes completas extraídas

Las siguientes secciones contienen la extracción completa de las seis versiones cargadas. CLAUDE CODE debe usarlas como respaldo literal para campos, tablas, prompts y reglas específicas.



---

# FUENTE V6: NeurOrientador_V6 (1).docx

**Rol de esta fuente:** Versión vigente/canónica para MVP con ManyChat, Make AI Agents, Gemini y Google Sheets.


ICN SALUD  ·  SISTEMA CLÍNICO DE TELEORIENTACIÓN NEUROLÓGICA

NeurOrientador + NeuroAsistente

Documentación Técnica de Implementación

Versión 6.0  ·  2026

| Stack tecnológico V6 WhatsApp Business API  ·  ManyChat  ·  Make (AI Agents)  ·  Gemini  ·  Google Sheets Canales de entrada WhatsApp Business API  ·  ManyChat Gestión operativa ManyChat (MVP)  →  Zoho CRM (evaluación a corto plazo) Base metodológica ICHD-3  ·  DSM-5-TR  ·  Guías ICN  ·  Modelo UNI de Evaluación de Riesgo |
| --- |

| Novedades V6 vs V5 Canales: WhatsApp + ManyChat como entrada y gestión operativa del MVP SLA obligatorio de 15 minutos para respuesta humana — medido y registrado automáticamente Supervisión diaria del NeuroAsistente por el Neuroasesor — no es autónomo Resumen diario del NeuroAsistente generado por el sistema al final de cada día Reporte diario del Neuroasesor — operación, clínica y comercial Hoja NEUROASESOR_INTERACCIONES — trazabilidad total de la intervención humana Priorización operativa formalizada en toda la lógica del sistema Preparación para Zoho CRM: modelo de datos compatible, análisis costo-beneficio incluido Análisis de formulario web para scoring F3 — propuesta de reducción de créditos de IA |
| --- |

DOCUMENTO 1 — CANALES Y GESTIÓN OPERATIVA

1.1 Canales de Recepción de Casos

El sistema V6 opera sobre dos canales de entrada complementarios que convergen en la misma lógica de procesamiento (Make + Gemini) y base de datos (Google Sheets).

| Canal | Rol y configuración en MVP |
| --- | --- |
| WhatsApp Business API | Canal principal de conversación clínica. Webhook permanente 24/7. Toda la lógica F0–F4 y NeuroAsistente opera sobre WhatsApp. Los mensajes llegan a Make vía webhook HTTP con verificación HMAC. |
| ManyChat | Canal de entrada complementario y panel de gestión operativa para el Neuroasesor. Recibe el primer contacto, puede pre-clasificar la intención (admin / clínico) antes de derivar al flujo de Make. Actúa como CRM ligero en el MVP. |

1.2 ManyChat como Panel de Gestión (MVP)

Durante el MVP, ManyChat cumple un doble rol: canal de primer contacto y herramienta de gestión para el Neuroasesor. Esto permite operar sin CRM completo hasta que el volumen justifique la migración.

| FUNCIONES DE MANYCHAT EN MVP Recepción y clasificación inicial de mensajes entrantes (admin / clínico) Vista consolidada de conversaciones activas para el Neuroasesor Gestión de etiquetas por estado: nuevo · en orientación · agendado · escalado · cerrado Transferencia a agente humano cuando el sistema activa HUMANO o escalamiento comercial Dashboard básico con filtros por estado, etiqueta y prioridad de paciente Integración con Make vía webhook para sincronización bidireccional de estados |
| --- |

1.3 Flujo Integrado WhatsApp + ManyChat + Make

| Paso | Descripción del flujo integrado |
| --- | --- |
| 1. Entrada | El paciente escribe por WhatsApp o ManyChat. |
| 2. Pre-clasificación | ManyChat detecta si es primer contacto o paciente existente. Puede aplicar filtro inicial de intención. |
| 3. Derivación a Make | ManyChat dispara el webhook de Make con los parámetros del mensaje. Make toma control del flujo clínico. |
| 4. Procesamiento | Make ejecuta filtro de alarma → AI Agent (Gemini) → lógica backend → actualización Sheets. |
| 5. Respuesta | Make envía la respuesta_visible al paciente por WhatsApp. ManyChat actualiza el estado del contacto. |
| 6. Escalamiento | Si hay escalamiento humano, Make notifica al Neuroasesor. ManyChat asigna la conversación al agente y registra prioridad. |

DOCUMENTO 2 — SLA DE RESPUESTA HUMANA: 15 MINUTOS

2.1 Definición del KPI Crítico

| KPI OBLIGATORIO — TIEMPO MÁXIMO DE RESPUESTA HUMANA El Neuroasesor tiene un máximo de 15 minutos para responder a cualquier caso escalado por el sistema. Este KPI es obligatorio, se mide automáticamente y su incumplimiento queda registrado. EXCEPCIÓN: Alarmas clínicas críticas (convulsión activa, ACV, pensamiento suicida) tienen un tiempo objetivo de respuesta inmediata < 5 minutos. |
| --- |

2.2 Medición Automática del SLA

Make registra el timestamp exacto de cada escalamiento y, cuando el Neuroasesor responde, calcula automáticamente el tiempo transcurrido. El campo cumple_sla_15min se actualiza sin intervención manual.

| Campo | Descripción |
| --- | --- |
| timestamp_escalamiento | Fecha y hora exacta en que Make notificó el escalamiento al Neuroasesor. Generado automáticamente. |
| timestamp_respuesta_humano | Fecha y hora en que el Neuroasesor envió la primera respuesta al paciente. Registrado por Make al detectar el mensaje saliente del agente. |
| tiempo_respuesta_humano | Diferencia en minutos entre timestamp_escalamiento y timestamp_respuesta_humano. Calculado por Make. Formato: número decimal. |
| cumple_sla_15min | TRUE si tiempo_respuesta_humano ≤ 15. FALSE si supera los 15 minutos. Calculado automáticamente por Make. No editable manualmente. |
| tipo_escalamiento | Clínico / Comercial / Solicitud_paciente / Error_sistema / Alarma_critica. Determina el SLA objetivo. |
| prioridad_sla | Alta (paciente agendado) / Media (particular) / Normal (resto). Influye en la urgencia de notificación al Neuroasesor. |

2.3 Lógica de Incumplimiento de SLA en Make

| FLUJO AUTOMÁTICO SI cumple_sla_15min = FALSE Registrar incumplimiento en hoja ESCALAMIENTOS con cumple_sla_15min = FALSE Enviar alerta interna al coordinador ICN: paciente, tipo de escalamiento, tiempo transcurrido Actualizar ManyChat: marcar conversación como 'vencida' en el panel del Neuroasesor Registrar en campo incidencias_sla del resumen diario del Neuroasesor Acumular para métricas semanales de calidad operativa |
| --- |

2.4 KPIs de SLA — Dashboard de Calidad

| Métrica | Descripción y umbral de alerta |
| --- | --- |
| % SLA cumplido (diario) | Porcentaje de escalamientos respondidos en ≤15 min en el día. Umbral mínimo aceptable: 90%. |
| Tiempo promedio de respuesta | Promedio de tiempo_respuesta_humano del día. Objetivo: < 8 minutos. |
| Escalamientos por turno | Número de casos escalados por franja horaria. Identifica horas de alta carga. |
| Incumplimientos acumulados | Total de cumple_sla_15min = FALSE en la semana. Dispara revisión de capacidad si supera 3. |
| SLA por tipo de escalamiento | Desglose por clínico, comercial, solicitud_paciente. Permite ajuste diferenciado. |

DOCUMENTO 3 — ROL DEL NEUROASESOR: SUPERVISIÓN, OPERACIÓN Y REPORTES

3.1 Definición del Rol Completo

El Neuroasesor no es únicamente quien atiende casos escalados. En el modelo V6, su rol es activo, supervisory y estratégico. Opera como el punto de control humano de todo el sistema.

| RESPONSABILIDADES DEL NEUROASESOR — V6 Responder escalamientos: Atender casos clínicos, comerciales o de error dentro del SLA de 15 minutos. Supervisar el NeuroAsistente: Revisar diariamente el resumen de interacciones automáticas, validar calidad y detectar anomalías. Validar calidad de interacción: Auditar conversaciones de Gemini para detectar respuestas incorrectas, tono inadecuado o errores clínicos. Detectar oportunidades comerciales: Identificar pacientes que podrían convertirse, reagendar o acceder a nuevos programas. Detectar problemas clínicos no resueltos: Identificar casos donde el paciente no recibió orientación adecuada o tiene síntomas sin seguimiento. Generar reporte diario: Documentar la gestión del día según el formato establecido en sección 3.3. |
| --- |

3.2 Supervisión Diaria del NeuroAsistente

| PRINCIPIO OPERATIVO — SUPERVISIÓN El NeuroAsistente NO es completamente autónomo. Debe ser supervisado diariamente por el Neuroasesor. La autonomía del sistema es operativa, no es supervisión cero. |
| --- |

Al final de cada día operativo, el sistema genera automáticamente un resumen de gestión del NeuroAsistente. Este resumen es la herramienta principal de supervisión del Neuroasesor.

| Elemento del resumen diario | Descripción |
| --- | --- |
| Pacientes contactados | Lista de todos los pacientes que recibieron mensaje del NeuroAsistente en el día, con nombre, tipo de interacción y hora de contacto. |
| Mensajes enviados | Texto completo de cada mensaje enviado, agrupado por paciente. |
| Respuestas del paciente | Respuesta exacta de cada paciente o 'sin_respuesta' con timestamp de vencimiento. |
| Casos con revisión clínica | Lista de interacciones donde requiere_revision_clinica = TRUE, con resumen de la señal detectada. |
| Casos con revisión comercial | Lista de interacciones donde requiere_revision_comercial = TRUE, con resumen de la oportunidad o señal. |
| Sin respuesta tras 24h | Pacientes que no respondieron y cuya interacción pasó a estado 'pendiente' o 'cerrado'. |
| Métricas del día | Total de interacciones, tasa de respuesta, tipos predominantes, casos escalados. |

3.3 Reporte Diario Obligatorio del Neuroasesor

Además del resumen del NeuroAsistente generado por el sistema, el Neuroasesor debe completar un reporte de su propia gestión al final de cada jornada. En el MVP puede ser manual; en fases posteriores se puede automatizar la plantilla desde Sheets.

| ESTRUCTURA DEL REPORTE DIARIO DEL NEUROASESOR Con quién habló: Lista de pacientes atendidos directamente por el Neuroasesor en el día. Temas tratados: Resumen del tipo de interacción por paciente: orientación clínica, cierre comercial, soporte, resolución de duda. Casos cerrados: Pacientes que concluyeron su proceso (agenda confirmada, rechazo definitivo, alta del programa). Casos abiertos: Pacientes que requieren seguimiento activo al día siguiente, con razón y próximo paso definido. Pacientes que requieren seguimiento: Lista priorizada de pacientes que el Neuroasesor considera prioritarios para el día siguiente. Incidencias relevantes: Cualquier evento fuera del flujo normal: error del sistema, queja, complicación clínica, SLA incumplido. Oportunidades detectadas: Pacientes con interés en nuevos programas, referencias, reagendas o ampliación de servicios. |
| --- |

DOCUMENTO 4 — TRAZABILIDAD COMPLETA DE INTERACCIONES HUMANAS

4.1 Principio de Registro Total

| TODO LO QUE HAGA EL NEUROASESOR DEBE QUEDAR REGISTRADO Así como el NeuroAsistente tiene la hoja NEUROASISTENTE_INTERACCIONES, el Neuroasesor tiene la hoja NEUROASESOR_INTERACCIONES. Ambas forman la capa de trazabilidad completa del sistema. |
| --- |

4.2 Hoja NEUROASESOR_INTERACCIONES — Esquema Completo

Una fila por cada intervención directa del Neuroasesor. Incluye tanto respuestas a escalamientos como contactos proactivos, supervisión y gestión comercial.

| Campo | Tipo | Descripción y reglas |
| --- | --- | --- |
| neuroasesor_interaccion_id | Texto (auto) | ID único. Formato: NA_H-{paciente_id}-{YYYYMMDDTHHmmss}. Distingue de interacciones automáticas del NeuroAsistente. |
| paciente_id | Texto | FK → PACIENTES. Obligatorio. |
| fecha_hora_inicio | Fecha-hora | Timestamp de inicio de la intervención del Neuroasesor. ISO 8601. |
| fecha_hora_fin | Fecha-hora | Timestamp de cierre de la intervención. Cuando el Neuroasesor marca el caso como cerrado o pendiente. |
| tiempo_respuesta_humano | Número | Minutos transcurridos desde el escalamiento hasta la primera respuesta. Calculado automáticamente por Make. |
| cumple_sla_15min | Booleano | TRUE si tiempo_respuesta_humano ≤ 15. FALSE si supera el SLA. Calculado automáticamente. |
| canal | Texto | Canal de la intervención: WhatsApp \| ManyChat \| Email \| Llamada. |
| tipo_interaccion | Texto | Valores: escalamiento_clinico \| escalamiento_comercial \| supervision_neuroasistente \| contacto_proactivo \| soporte \| cierre_comercial. |
| prioridad_paciente | Texto | Nivel de prioridad: agendado \| particular \| general. Copiado de PACIENTES. |
| resumen_conversacion | Texto | Descripción del Neuroasesor sobre el contenido de la interacción. Obligatorio en todos los casos. |
| resultado | Texto | Valores: cerrado \| pendiente \| escalado_medico \| nueva_cita_agendada \| rechazo \| sin_respuesta. |
| oportunidad_detectada | Texto | Descripción de oportunidad comercial o clínica identificada. Vacío si no aplica. |
| incidencia | Texto | Descripción de incidencia relevante (error sistema, queja, complicación). Vacío si no aplica. |
| notas_internas | Texto | Observaciones del Neuroasesor para el equipo ICN. No se comparte con el paciente. |
| responsable | Texto | Nombre o ID del Neuroasesor que atendió. Permite análisis por agente. |
| version_flujo | Texto | Versión del flujo activa en el momento. Ejemplo: v6.0. |

DOCUMENTO 5 — RESUMEN DIARIO DEL NEUROASISTENTE

5.1 Flujo de Generación Automática

Al final de cada día operativo (configurable, por defecto 8:00 PM hora Colombia), Make ejecuta un escenario de resumen que consolida toda la actividad del NeuroAsistente y la envía al Neuroasesor para revisión.

| Paso | Acción en Make — Escenario Resumen Diario |
| --- | --- |
| 1 | TRIGGER — Schedule diario a las 8:00 PM (UTC-5, Colombia). Ejecutar de lunes a sábado. |
| 2 | GOOGLE SHEETS — Filtrar hoja NEUROASISTENTE_INTERACCIONES por fecha_hora del día actual. |
| 3 | Agrupar resultados por: tipo_interaccion, estado_interaccion, requiere_revision_clinica, requiere_revision_comercial. |
| 4 | AI AGENT (Gemini) — Generar resumen narrativo del día con los datos filtrados. Prompt: 'Genera un resumen ejecutivo del día del NeuroAsistente con estos datos. Tono: operativo, claro, directo. Incluye alertas si hay casos clínicos o comerciales pendientes.' |
| 5 | Calcular métricas: total interacciones, % respondido, # casos clínicos, # casos comerciales, # sin respuesta. |
| 6 | WHATSAPP / EMAIL — Enviar resumen al Neuroasesor con formato estructurado. |
| 7 | GOOGLE SHEETS — Insertar fila en hoja RESUMENES_DIARIOS con las métricas del día. |

5.2 Formato del Resumen Diario

| PLANTILLA — RESUMEN DIARIO NEUROASISTENTE 📊 RESUMEN DEL DÍA — NEUROASISTENTE · ICN Salud Fecha: [fecha]  ·  Generado: [timestamp] ACTIVIDAD DEL DÍA • Total de pacientes contactados: [N] • Total de mensajes enviados: [N] • Pacientes que respondieron: [N] ([%]%) • Sin respuesta: [N] TIPOS DE INTERACCIÓN • Confirmaciones de cita: [N]  \|  Preparaciones: [N]  \|  Recordatorios: [N]  \|  Seguimientos post cita: [N] ⚠️ REQUIEREN ATENCIÓN • Revisión clínica requerida: [N pacientes] — [lista con nombres y señal detectada] • Revisión comercial requerida: [N pacientes] — [lista con nombres y oportunidad/señal] • Sin respuesta (>24h): [N pacientes] — [lista con nombres] |
| --- |

DOCUMENTO 6 — PRIORIZACIÓN OPERATIVA

6.1 Orden de Atención — Regla Obligatoria

| ORDEN DE PRIORIDAD OPERATIVA — V6 Pacientes que ya agendaron con ICN Salud — Máxima prioridad. NeuroAsistente activo. Toda alarma o escalamiento se atiende primero. Pacientes particulares — Segunda prioridad. En proceso de evaluación o conversión activa. Respuesta preferencial. Otros pacientes — Tercera prioridad. Contactos iniciales, evaluaciones sin agenda confirmada. |
| --- |

6.2 Aplicación de la Prioridad en el Sistema

| Componente | Cómo se aplica la priorización |
| --- | --- |
| SLA de respuesta | Pacientes agendados generan alerta inmediata al Neuroasesor. Particulares tienen 10 min de gracia antes de segunda alerta. Resto: 15 min estándar. |
| Escalamiento en Make | El campo prioridad_sla se incluye en toda notificación de escalamiento. ManyChat ordena la bandeja por este campo. |
| NeuroAsistente | El campo prioridad_paciente en NEUROASISTENTE_INTERACCIONES permite filtrar y priorizar el resumen diario. |
| Cola de seguimiento | El Neuroasesor revisa primero los casos de pacientes agendados, luego particulares. El sistema ordena los reportes bajo este criterio. |
| Asignación de agenda | Cuando hay slots disponibles limitados, se ofrece primero a pacientes de mayor prioridad. |

DOCUMENTO 7 — PROTOCOLO DE ESCALAMIENTO HUMANO

7.1 Información Obligatoria en Todo Escalamiento

| PROTOCOLO DE ESCALAMIENTO — DATOS OBLIGATORIOS Cuando Make activa un escalamiento (clínico, comercial o de error), debe enviar al Neuroasesor la siguiente información de forma estructurada y completa. No se puede escalar sin estos campos. Nombre: Nombre completo del paciente capturado en F1. Teléfono: Número de WhatsApp del paciente para contacto directo. Problema principal: Problema neurológico seleccionado en F2 (ej: Cefalea, Epilepsia). Nivel de riesgo: Clasificación calculada por Make: Bajo / Moderado / Alto / Alarma. Resumen clínico: notas_internas del último turno de F3 generadas por Gemini. Motivo del escalamiento: Descripción precisa: tipo de alarma, señal comercial, solicitud del paciente, error del sistema. Prioridad del paciente: Agendado / Particular / General — para que el Neuroasesor priorice su respuesta. Fase en que ocurrió: F2, F3, F4 o NeuroAsistente — proporciona contexto del momento del proceso. |
| --- |

7.2 Tipos de Escalamiento y Tiempos Objetivo

| Tipo de escalamiento | Tiempo objetivo de respuesta / Acción |
| --- | --- |
| Alarma clínica crítica | < 5 minutos. Palabras clave de riesgo de vida. Orientar a urgencias + notificar Neuroasesor inmediatamente. |
| Escalamiento clínico (D1 ≥ 2) | ≤ 15 minutos. Banderas rojas detectadas en F3. Neuroasesor evalúa el caso. |
| Escalamiento comercial (F4) | ≤ 15 minutos. Paciente duda, pide precio repetidamente o pide hablar con persona. |
| Solicitud del paciente | ≤ 15 minutos. El paciente pide explícitamente hablar con un humano. |
| Error del sistema (JSON persistente) | ≤ 15 minutos. Sistema no pudo procesar. Neuroasesor continúa la conversación manualmente. |
| Señal en NeuroAsistente (clínica) | ≤ 15 minutos. Complicación post-cita, duda médica, angustia expresada. |
| Señal en NeuroAsistente (comercial) | ≤ 30 minutos. Cancelación, interés en nuevo programa, inconformidad. |

DOCUMENTO 8 — ANÁLISIS Y RECOMENDACIÓN DE CRM

8.1 Contexto de la Decisión

El MVP opera sobre ManyChat + Google Sheets. A medida que el volumen crece y la gestión comercial se complejiza, se requiere evaluar la migración a un CRM. Este documento presenta el análisis costo-beneficio de las opciones más relevantes para el contexto de ICN Salud, con una recomendación clara.

8.2 Criterios de Evaluación

| Criterio | Importancia para ICN Salud |
| --- | --- |
| Integración con WhatsApp | Crítica — el canal principal es WhatsApp. |
| Integración con Make | Crítica — toda la automatización corre en Make. |
| Integración con ManyChat | Alta — ManyChat es el panel de gestión actual. |
| Facilidad de uso para el Neuroasesor | Alta — el equipo no es técnico. |
| Pipeline de ventas / agenda | Alta — F4 es conversión activa. |
| Costo mensual (volumen ~500 pacientes) | Alta — debe ser sostenible en MVP. |
| Curva de implementación | Media — debe poder configurarse en 2-4 semanas. |
| Compatibilidad con modelo de datos actual | Alta — migración limpia desde Sheets. |
| Soporte y documentación en español | Media — contexto latinoamericano. |

8.3 Comparativo de CRMs

| Criterio | Zoho CRM | HubSpot CRM | Pipedrive | Kommo (ex amoCRM) | Brevo CRM |
| --- | --- | --- | --- | --- | --- |
| Integración WhatsApp | ✅ Nativa | ⚠️ Vía Zapier | ⚠️ Vía Make | ✅ Nativa (líder) | ⚠️ Limitada |
| Integración Make | ✅ Módulo oficial |  |  |  | ⚠️ HTTP genérico |
| Integración ManyChat | ⚠️ Vía webhook |  |  | ✅ Integración directa | ⚠️ Vía webhook |
| Pipeline / Agenda | ✅ Completo |  | ✅ Excelente | ✅ Bueno | ⚠️ Básico |
| Facilidad de uso | ⚠️ Curva media | ✅ Muy fácil |  | ✅ Fácil |  |
| Costo ~500 contactos/mes | US$14–20/usr | US$0 (Free) / US$15 | US$12–24/usr | US$15/usr | US$0–25/mes |
| Curva implementación | 3–5 semanas | 1–2 semanas |  | 2–3 semanas | 1–2 semanas |
| Soporte en español | ✅ Sí |  |  |  |  |
| Adecuación al caso ICN | Alta | Media-Alta | Media | Muy Alta | Media |

8.4 Recomendación Principal: Kommo (ex amoCRM)

| CRM RECOMENDADO PARA ICN SALUD: KOMMO Kommo (anteriormente amoCRM) es el CRM más adecuado para el contexto de ICN Salud por una razón central: es el único CRM de la región diseñado nativamente para gestión de conversaciones por mensajería (WhatsApp, Instagram, Telegram), con pipeline visual y automatización incluida. Es ampliamente usado en equipos de salud privada en Latinoamérica que gestionan pacientes por WhatsApp. |
| --- |

Por qué Kommo es la mejor opción:

WhatsApp nativo: La bandeja de Kommo integra WhatsApp directamente — el Neuroasesor ve todas las conversaciones en un solo lugar sin salir del CRM.

Pipeline visual: Gestión de pacientes por etapa: Nuevo → En orientación → F3 completado → Agendado → Consulta realizada → Seguimiento. Perfecto para el flujo de NeurOrientador.

Integración con Make: Módulo oficial en Make. La sincronización de PACIENTES (Sheets) → Contactos (Kommo) es directa y mantenible.

Integración con ManyChat: Kommo y ManyChat tienen integración directa. No requiere webhooks personalizados.

Automatizaciones internas: Kommo tiene su propio motor de automatización para tareas básicas dentro del CRM (mover etapas, asignar, notificar).

Costo real para ICN: Plan Base: US$15/usuario/mes. Con 1-2 Neuroasesores: US$15–30/mes. Sin costo fijo por número de contactos.

Curva de implementación: 2–3 semanas para configuración completa con Make. La UI es intuitiva para el equipo operativo.

Alternativa sólida: Zoho CRM

Zoho CRM es la segunda opción más completa. Su ventaja es el ecosistema Zoho (Zoho Desk, Zoho Books, Zoho Analytics), lo que permite crecer sin cambiar de plataforma. Su desventaja frente a Kommo es que la integración con WhatsApp requiere configuración adicional (Zoho SalesIQ o API propia) y la curva de implementación es más larga.

Recomendable si ICN Salud anticipa necesidades de facturación electrónica, soporte estructurado (tickets) o reportería analítica avanzada a 12-18 meses. En ese escenario, el ecosistema Zoho ofrece mayor retorno de la inversión de configuración.

8.5 Hoja de Ruta de Migración MVP → CRM

| Fase | Descripción y criterio de activación |
| --- | --- |
| Fase 1 — MVP (actual) | ManyChat + Google Sheets. Operar hasta los primeros 150-200 pacientes activos o hasta que la gestión manual del Neuroasesor se vuelva ineficiente (>3h/día de gestión). |
| Fase 2 — Evaluación (mes 2-3) | Instalar Kommo en prueba gratuita. Configurar pipeline, integrar WhatsApp. Probar en paralelo con Sheets sin migrar datos aún. |
| Fase 3 — Migración (mes 3-4) | Exportar PACIENTES de Sheets a Kommo. Configurar Make para escribir en Kommo en lugar de (o además de) Sheets. Mantener Sheets como registro clínico. |
| Fase 4 — Operación CRM (mes 4+) | Kommo como panel principal del Neuroasesor. Sheets como base de datos clínica. Make como orquestador central. Zoho como opción si se requiere ecosistema completo. |

8.6 Modelo de Datos Compatible con CRM

El esquema de datos de PACIENTES en Google Sheets está diseñado para migración directa. Cada campo tiene equivalente en Kommo y Zoho CRM.

| Campo en Sheets (ICN) | Equivalente en Kommo / Zoho CRM |
| --- | --- |
| paciente_id | Contact ID (Kommo) / Account ID (Zoho) |
| telefono | Phone (campo principal de contacto) |
| nombre | Contact Name |
| fase_actual | Pipeline Stage (etapa del embudo) |
| nivel_riesgo | Custom Field: nivel_riesgo (texto) |
| programa_clinico | Custom Field: programa_clinico |
| prioridad_operativa | Lead Score / Tag de prioridad |
| canal_agenda | Custom Field: canal_agenda |
| conversion | Deal / Opportunity |
| fecha_cita | Activity: Appointment |
| requiere_humano | Task asignada al Neuroasesor |
| notas_internas | Notes del contacto |

DOCUMENTO 9 — ANÁLISIS: FORMULARIO WEB PARA SCORING F3

9.1 La Propuesta

El cliente propone reemplazar la lógica conversacional de F3 (árbol clínico D1-D6 via Gemini) por un formulario web dinámico que ejecute el scoring de forma determinista, clasifique el nivel de riesgo y retorne el resultado a Make para continuar el flujo. El objetivo principal es reducir el consumo de créditos de IA en el tramo de mayor uso del sistema.

9.2 Análisis Técnico: ¿Qué parte de F3 realmente necesita IA?

| Componente de F3 | ¿Necesita IA Gemini? |
| --- | --- |
| Cálculo del score D1-D6 | NO — es determinista. Puntaje fijo por respuesta. Un formulario web lo ejecuta perfectamente. |
| Clasificación nivel_riesgo | NO — umbrales fijos calculables en JS. No requiere IA. |
| Asignación fenotipo y CIE-10 | Parcialmente — se puede implementar como lookup table en JS para los fenotipos más frecuentes. |
| Validación emocional entre preguntas | SÍ — requiere IA para adaptar el tono según lo que el paciente describe. |
| Detección de banderas rojas en texto libre | SÍ — si el paciente escribe respuestas libres, se necesita IA para interpretar. |
| Adaptación de lenguaje por contexto | SÍ — si el formulario es de selección múltiple pura, no se necesita IA. |

9.3 Comparativo: Conversacional vs Formulario Web

| Criterio | F3 Conversacional (actual) | F3 Formulario Web |
| --- | --- | --- |
| Costo por evaluación | ~800 tokens Gemini por turno × 5-6 turnos = 4.000-5.000 tokens | Costo cero de IA — todo en JS del formulario |
| Experiencia del paciente | Alta — se siente guiado y acompañado | Media — más eficiente pero menos cálida |
| Validación emocional | ✅ Presente en cada turno | ❌ No hay validación emocional automática |
| Tiempo de completar F3 | 5-8 minutos (conversacional) | 2-3 minutos (formulario) |
| Detección de señales de riesgo | ✅ Gemini detecta señales en texto libre | ⚠️ Solo si el paciente selecciona la opción correcta |
| Integración con Make | Ya implementado | Requiere endpoint webhook en formulario |
| Tasa de abandono esperada | Baja — conversación guiada retiene al paciente | Media-Alta — formularios web tienen 40-60% de abandono |
| Consistencia de respuestas | Media — el paciente puede dar respuestas ambiguas | Alta — opciones estructuradas de selección múltiple |
| Tiempo de implementación | Ya implementado | 2-3 semanas de desarrollo web |

9.4 Propuesta Híbrida — La Mejor Opción

| RECOMENDACIÓN: MODELO HÍBRIDO F3 No es una decisión binaria (conversacional o formulario). La propuesta óptima combina lo mejor de ambos: el formulario ejecuta el scoring y devuelve el resultado a Make, y Gemini solo interviene en los puntos donde agrega valor real. |
| --- |

Modelo Híbrido — Cómo funciona:

| Paso | Responsable y descripción |
| --- | --- |
| 1. WhatsApp (F0-F2) | Gemini maneja la conversación de clasificación, consentimiento y selección de problema. Sin cambios. |
| 2. Link al formulario (al inicio de F3) | Make envía al paciente un link personalizado con token único: 'Para continuar tu evaluación, completa este formulario corto: [link]'. El formulario carga con los datos del paciente ya capturados (nombre, programa). |
| 3. Formulario web dinámico | El paciente responde D1-D6 con opciones de selección múltiple + campo de texto libre opcional. El formulario tiene lógica JS que calcula el score en tiempo real y muestra retroalimentación visual. |
| 4. Webhook a Make | Al enviar el formulario, dispara un webhook a Make con: score_total, puntajes D1-D6, respuestas_orientacion, fenotipo_probable, nivel_riesgo, cie10. |
| 5. Make retoma el flujo | Con los datos del formulario, Make actualiza PACIENTES, activa F4 si corresponde o escala a HUMANO si hay alarma. Gemini solo se llama si el score es Alarma (para mensaje empático personalizado). |
| 6. Gemini en F4 | Gemini retoma la conversación en WhatsApp para la fase de conversión con todos los datos del scoring ya calculados. Sin necesidad de re-evaluar. |

9.5 Ahorro Estimado de Créditos

| Escenario | Consumo estimado de tokens Gemini |
| --- | --- |
| F3 conversacional (actual) | ~4.000-5.000 tokens por paciente en F3 (5-6 turnos × 800 tokens) |
| Modelo híbrido con formulario | ~0 tokens en F3. Gemini solo en F0-F2 (~2.400 tokens) y F4 (~1.600 tokens) = ~4.000 tokens totales |
| Ahorro por paciente | ~4.000-5.000 tokens por evaluación completada |
| Ahorro a 500 pacientes/mes | ~2.000.000-2.500.000 tokens mensuales. Equivale a reducir el costo de IA entre un 40-50%. |
| Tiempo de desarrollo formulario | 2-3 semanas. Recomendado para Fase 2 del proyecto (post-MVP estabilizado). |

9.6 Decisión Recomendada

| DECISIÓN Y HOJA DE RUTA MVP (ahora): Mantener F3 conversacional con Gemini. El formulario requiere desarrollo adicional que puede demorar el lanzamiento. Prioridad: operar y aprender. Fase 2 (mes 2-3): Desarrollar el formulario web dinámico en paralelo a la operación. Recomendado en Typeform, Tally o desarrollo propio con webhook. Integrar a Make y probar con un grupo piloto de pacientes. Fase 3 (mes 4+): Migrar F3 al modelo híbrido con el formulario como ruta principal. Mantener F3 conversacional como opción alternativa para pacientes que prefieran WhatsApp sin abrir links. |
| --- |

DOCUMENTO 10 — MODELO DE DATOS V6

10.1 Hojas del Sistema — Inventario Completo V6

| Hoja | Propósito y estado |
| --- | --- |
| PACIENTES | Registro principal por paciente. Una fila por paciente. Clave primaria: telefono. Actualizada en cada turno. ✅ Existente — sin cambios estructurales en V6. |
| CONVERSACIONES | Auditoría de cada turno del flujo F0-F4. Una fila por turno. ✅ Existente — sin cambios en V6. |
| CITAS | Una fila por cita agendada. Alimenta el NeuroAsistente. ✅ Existente — sin cambios en V6. |
| COHORTES_INVESTIGACION | Datos anonimizados de evaluaciones completadas. Solo si consentimiento_investigacion = TRUE. ✅ Existente — sin cambios en V6. |
| NEUROASISTENTE_INTERACCIONES | Trazabilidad de cada interacción automática del NeuroAsistente. ✅ Existente (V4.1) — campo prioridad_paciente y prioridad_sla añadidos en V6. |
| NEUROASESOR_INTERACCIONES | 🆕 NUEVA EN V6. Trazabilidad de cada intervención directa del Neuroasesor. Ver Documento 4 para esquema completo. |
| ESCALAMIENTOS | 🆕 NUEVA EN V6. Registro de todos los escalamientos con SLA. Ver campos en sección 10.2. |
| RESUMENES_DIARIOS | 🆕 NUEVA EN V6. Una fila por día con métricas consolidadas del NeuroAsistente y Neuroasesor. |

10.2 Hoja ESCALAMIENTOS — Esquema

Registro de cada escalamiento generado por el sistema, con medición de SLA y tipo de incidencia.

| Campo | Tipo y descripción |
| --- | --- |
| escalamiento_id | Texto (auto). Formato: ESC-{paciente_id}-{timestamp}. |
| paciente_id | FK → PACIENTES. |
| timestamp_escalamiento | Fecha-hora exacta de activación del escalamiento por Make. |
| timestamp_respuesta_humano | Fecha-hora de primera respuesta del Neuroasesor. |
| tiempo_respuesta_humano | Minutos entre escalamiento y respuesta. Calculado por Make. |
| cumple_sla_15min | Booleano. TRUE si ≤ 15 min. FALSE si supera el SLA. |
| tipo_escalamiento | alarma_critica \| clinico \| comercial \| solicitud_paciente \| error_sistema \| neuroasistente_clinico \| neuroasistente_comercial |
| prioridad_paciente | agendado \| particular \| general — copiado de PACIENTES en el momento del escalamiento. |
| fase_origen | Fase en que ocurrió: F2 \| F3 \| F4 \| NeuroAsistente. |
| motivo | Descripción del motivo del escalamiento. |
| resolucion | Texto libre del Neuroasesor describiendo cómo se resolvió. |
| responsable | Nombre del Neuroasesor que atendió. |
| resultado | cerrado \| pendiente \| derivado_medico \| cita_agendada. |

10.3 Hoja RESUMENES_DIARIOS — Esquema

| Campo | Descripción |
| --- | --- |
| resumen_id | ID único: RES-{YYYYMMDD}. |
| fecha | Fecha del resumen. |
| total_interacciones_na | Total de interacciones del NeuroAsistente en el día. |
| total_respondidas | Pacientes que respondieron al NeuroAsistente. |
| total_sin_respuesta | Pacientes que no respondieron en 24h. |
| casos_revision_clinica | Número de casos con requiere_revision_clinica = TRUE. |
| casos_revision_comercial | Número de casos con requiere_revision_comercial = TRUE. |
| total_escalamientos | Total de escalamientos al Neuroasesor en el día. |
| sla_cumplido_pct | Porcentaje de escalamientos atendidos en ≤ 15 min. |
| tiempo_respuesta_promedio | Promedio de tiempo_respuesta_humano del día en minutos. |
| total_interacciones_neuroasesor | Total de filas en NEUROASESOR_INTERACCIONES del día. |
| resumen_narrativo | Texto generado por Gemini con el resumen ejecutivo del día. |
| incidencias_sla | Número de incumplimientos de SLA del día. |
| oportunidades_detectadas | Número de oportunidades comerciales registradas. |

RESUMEN EJECUTIVO V6 — DECISIONES Y ESTADO DEL SISTEMA

Qué se implementa en V6

| ✅ IMPLEMENTADO EN V6 (MVP) Canales: WhatsApp Business API + ManyChat como entrada y gestión operativa SLA de 15 minutos para respuesta humana — medido automáticamente por Make Campos: tiempo_respuesta_humano y cumple_sla_15min en hoja ESCALAMIENTOS NeuroAsistente supervisado — no autónomo — con resumen diario automático a las 8 PM Rol del Neuroasesor ampliado: supervisión + operación + comercial + calidad Reporte diario del Neuroasesor — manual en MVP, apoyado en datos de Sheets Hoja NEUROASESOR_INTERACCIONES — trazabilidad total de intervenciones humanas Hoja ESCALAMIENTOS — registro y medición de SLA por escalamiento Hoja RESUMENES_DIARIOS — métricas consolidadas diarias Priorización operativa integrada en lógica de Make, ManyChat y reportes Modelo de datos compatible con Kommo CRM y Zoho CRM para migración limpia |
| --- |

| 📋 RECOMENDACIONES A CORTO PLAZO CRM recomendado: Kommo (ex amoCRM) — mejor integración WhatsApp + pipeline + Make para el perfil de ICN Salud Alternativa: Zoho CRM — si se anticipa ecosistema completo (facturación, soporte, analytics) a 12-18 meses Formulario web para F3: implementar en Fase 2 (mes 2-3) — ahorro estimado 40-50% de créditos de IA Modelo híbrido F3: mantener conversacional como opción + formulario como ruta principal en Fase 3 Revisión de SLA en semana 4 de operación para ajustar umbrales y capacidad del Neuroasesor |
| --- |



---

# FUENTE V5: NeurOrientador_V5 (2).docx

**Rol de esta fuente:** Base operativa inmediatamente anterior; conservar reglas no contradichas por V6.


ICN SALUD — SISTEMA CLÍNICO DE TELEORIENTACIÓN NEUROLÓGICA

NeurOrientador

+ NeuroAsistente

Documentación Técnica de Implementación

Versión 5.0  ·  2026

| Stack tecnológico WhatsApp Business API  ·  Make  ·  ChatGPT API (GPT-4o)  ·  Google Sheets Base metodológica ICHD-3  ·  DSM-5-TR  ·  Guías ICN  ·  Modelo UNI de Evaluación de Riesgo  ·  2026 Fases implementadas en V5 F0 · F1 · F2 · F3 · F4 + NeuroAsistente (acompañamiento completo) Fases pospuestas F5 · F6 · ESRI · Investigación avanzada · Cohortes complejas |
| --- |

| NOTA DE VERSIÓN V5.0 Esta versión incorpora los ajustes operativos finales sobre V4.1: Seguimiento post consulta definido en 1 día después de la cita Disponibilidad 24/7 explícita como regla operativa Sistema de priorización operativa formalizado (3 niveles) Tono del sistema: clínico + humano + comercial (tríada obligatoria) F3 con posibilidad de cierre anticipado por suficiencia clínica F4 redefinida como fase de conversión explícita con escalamiento comercial NeuroAsistente: flujo de acompañamiento formal, trazabilidad total y retroalimentación Nota operativa: volumen inicial ~500 pacientes |
| --- |

DOCUMENTO 1 — ALCANCE Y DECISIONES OPERATIVAS MVP

1. Objetivo del MVP

| OBJETIVO DEL MVP Un sistema que recibe pacientes · realiza teleorientación · clasifica riesgo · genera confianza · convierte a cita — y acompaña al paciente antes y después de la consulta. |
| --- |

2. Fases del MVP — Qué Entra y Qué No Entra

| ✅ INCLUIDO EN MVP | 🚫 EXCLUIDO DEL MVP |
| --- | --- |
| F0 | Clasificación inicial de intención del contacto |
| F1 | Consentimiento e identificación del paciente |
| F2 | Selección de problema neurológico |
| F3 | Teleorientación clínica estructurada (scoring) |
| F4 | Conversión a cita — fase comercial explícita |
| NeuroAsistente | Acompañamiento formal post-agenda (confirmación, preparación, recordatorio, seguimiento) |
| Excluidos | F5 — Seguimiento automático de citas F6 — Educación recurrente preventiva ESRI — Contexto geográfico/socioeconómico Modelos predictivos / cohortes complejas / investigación avanzada |

| REGLA FUNDAMENTAL — NO NEGOCIABLE Todo paciente debe completar F3 antes de agendar. No se puede saltar F3 aunque el paciente llegue preguntando por precio o cita directamente. Una teleconsulta = un problema neurológico. Si hay múltiples, se agenda una teleconsulta separada para cada uno. |
| --- |

3. Decisiones de Diseño Críticas

3.1 Lógica clínica separada de ChatGPT

| RESPONSABILIDAD DE MAKE (backend) | RESPONSABILIDAD DE ChatGPT (IA) |
| --- | --- |
| Make calcula | score_total (suma D1–D6), nivel_riesgo, flag_alarma, transición de fases, validación JSON, filtro de alarmas |
| ChatGPT genera | respuesta_visible (texto al paciente), notas_internas (síntesis clínica), puntaje_dominio, tono adaptado al contexto |

3.2 Reporte de Riesgo — MVP

| MVP (implementar ahora) | V2 (posponer) |
| --- | --- |
| Formato | Mensaje WhatsApp estructurado con: nombre, programa, nivel de riesgo, fenotipo, recomendación, disclaimer legal |
| V2 | Imagen generada (Bannerbear / HTML-to-image) con branding ICN |

3.3 Lenguaje del Sistema — Ajuste Obligatorio

| ❌ LENGUAJE ANTERIOR (eliminar) | ✅ LENGUAJE CORRECTO (usar) |
| --- | --- |
| 'evidencia clínica validada' | 'base inicial para análisis clínico' |
| 'base de investigación consolidada' | 'datos estructurados para futura validación' |
| 'sistema clínico validado' | 'herramienta de orientación en etapa inicial' |

4. Reglas Operativas del Sistema — V5

4.1 Disponibilidad 24/7 — Regla Operativa

| REGLA OPERATIVA — DISPONIBILIDAD DEL SISTEMA Los pacientes pueden escribir a cualquier hora del día o de la noche. El sistema opera 24 horas al día, 7 días a la semana, sin excepción. Esta disponibilidad aplica tanto para NeurOrientador (flujo de orientación F0–F4) como para NeuroAsistente (acompañamiento post-agenda). No existen franjas horarias restringidas para el paciente. Los mensajes recibidos fuera del horario laboral del equipo ICN son procesados automáticamente por el sistema; las notificaciones de escalamiento humano se atienden según el protocolo de turno definido por ICN. |
| --- |

4.2 Priorización Operativa — Orden de Atención

El sistema opera bajo un criterio explícito de priorización para el seguimiento, el escalamiento, los tiempos de respuesta y el acompañamiento del NeuroAsistente. Este criterio es obligatorio y debe respetarse en toda la lógica de enrutamiento de Make.

| ORDEN DE PRIORIDAD OPERATIVA Pacientes que ya agendaron con ICN Salud — máxima prioridad. Tienen NeuroAsistente activo. Toda alarma o solicitud de este grupo se atiende primero. Pacientes particulares — segunda prioridad. En proceso de evaluación o conversión. Respuesta en el menor tiempo posible. Resto de pacientes — tercera prioridad. Incluye contactos iniciales en F0/F1 y pacientes en evaluación sin agenda confirmada. |
| --- |

Este orden se aplica a:

Frecuencia y urgencia de seguimiento por el NeuroAsistente

Tiempo de respuesta ante mensajes entrantes fuera de flujo automático

Prioridad de notificación al equipo ICN cuando hay escalamiento humano

Asignación de capacidad de agenda disponible

4.3 Nota Operativa — Volumen Inicial

| CONTEXTO DE VOLUMEN — V5 El sistema está diseñado inicialmente para operar con un volumen aproximado de 500 pacientes activos. Este contexto tiene implicaciones operativas directas: La trazabilidad completa es obligatoria — a este volumen es manejable y permite retroalimentación de alta calidad. La priorización operativa es obligatoria — garantiza que los pacientes agendados reciban atención preferencial. El acompañamiento de pacientes agendados es el eje central de retención y satisfacción. No hay límite rígido de mensajes: se envían los mensajes que sean necesarios según el caso y el momento del paciente. |
| --- |

DOCUMENTO 2 — TONO DEL SISTEMA

5. Tríada de Tono Obligatoria

El tono del sistema NeurOrientador / NeuroAsistente no es clínico ni empático de forma aislada. Todo mensaje que el sistema produzca — ya sea en orientación, seguimiento o acompañamiento — debe integrar simultáneamente tres componentes. Esta tríada es innegociable y aplica a todos los prompts y mensajes del sistema.

| CLÍNICO | HUMANO | COMERCIAL |
| --- | --- | --- |
| Transmite confianza y seriedad El paciente siente que está siendo atendido por un sistema profesional y riguroso. | Transmite cercanía, calidez y acompañamiento El paciente siente que hay alguien que le entiende y le cuida, no una máquina fría. | Orienta hacia la acción sin presión agresiva El paciente entiende qué debe hacer a continuación y siente que es el paso natural y correcto. |

6. Aplicación por Fase y Componente

| Fase / Componente | Cómo se aplica la tríada |
| --- | --- |
| F3 — Teleorientación | El componente clínico lidera: preguntas estructuradas, validación técnica. El humano está siempre presente: cada pregunta valida emocionalmente antes de avanzar ('Entiendo que esto ha sido difícil…'). El comercial es sutil: al cerrar F3, el tono prepara naturalmente la transición hacia la evaluación especializada. |
| F4 — Conversión | El clínico ancla la propuesta en hallazgos reales ('Con base en lo que me contaste…'). El humano mantiene calidez sin frialdad transaccional. El comercial es explícito y directo: propuesta concreta, horarios reales, cierre sin ambigüedad. |
| NeuroAsistente — Seguimiento | El humano lidera: el mensaje suena como alguien que de verdad está pendiente. El clínico garantiza credibilidad. El comercial es mínimo pero presente: si hay oportunidad de reagendar o nueva consulta, se facilita naturalmente. |
| Mensajes de recordatorio | Cálidos, breves, útiles. Recuerdan la cita con tono de acompañamiento, no de notificación automática. |

7. Principio del NeuroAsistente — Acompañamiento Cercano

| DEFINICIÓN DE TONO DEL NEUROASISTENTE El NeuroAsistente debe sentirse como el acompañamiento de alguien cercano y de confianza — casi como un familiar bien informado que está pendiente del proceso — pero manteniendo en todo momento la credibilidad clínica de ICN Salud y ayudando al paciente a avanzar en su camino de atención. El paciente debe sentir que puede escribir cuando lo necesite y que alguien real está al otro lado del proceso. |
| --- |

DOCUMENTO 3 — FLUJOS MAKE

8. Escenarios Make — MVP V5

| Escenario | Propósito / Estado |
| --- | --- |
| Escenario 1 | Conversación principal (F0–F4) — ✅ Activo 24/7 |
| Escenario 2 | Reporte estructurado de riesgo al cierre de F3 — ✅ Activo (texto, sin imagen en MVP) |
| Escenario 3 — NeuroAsistente | Flujo de acompañamiento: confirmación → preparación → recordatorio → seguimiento post consulta (1 día después) — ✅ Activo |
| Escenario 4 / 5 | F5 (seguimiento automático) y F6 (educación preventiva) — 🚫 Pospuestos V2 |

9. Escenario 1 — Conversación Principal (Detallado)

| TRIGGER: Webhook HTTP ← WhatsApp Business API  \|  Activo 24 horas al día, 7 días a la semana |
| --- |

| Paso | Acción en Make |
| --- | --- |
| 1 | WEBHOOK — Recibir mensaje. Parsear: numero_telefono, mensaje_texto, timestamp. Verificar firma HMAC. |
| 2 | FILTRO ALARMA (ANTES de ChatGPT) — Buscar palabras clave en el mensaje bruto. Si se detecta alarma → IR A PASO 14 DIRECTO. NO llamar a ChatGPT. Palabras clave: convulsión, pérdida de conciencia, no puedo mover, peor dolor de mi vida, rigidez de nuca, pensamiento suicida, cefalea en trueno, visión doble súbita, no puedo hablar. |
| 3 | GOOGLE SHEETS — Buscar paciente por teléfono (clave primaria). Si no existe → Paso 4a. Si existe → Paso 4b. |
| 4a | GOOGLE SHEETS — Crear nuevo paciente: telefono, fecha_creacion, fase_actual=F0, historial_json=[], consentimientos=FALSE. |
| 4b | GOOGLE SHEETS — Leer datos del paciente: fase_actual, historial_json, programa_clinico, nivel_riesgo, nombre, consentimientos, version_prompt, version_flujo, tipo_aseguramiento. |
| 5 | JSON PARSE — Deserializar historial_json. Truncar a máximo 15–20 turnos. |
| 6 | ROUTER — Seleccionar system prompt por fase_actual (F0, F1, F2, F3, F4, ADMIN, HUMANO). Registrar version_prompt y version_flujo activos. |
| 7 | ChatGPT API (GPT-4o) — Llamar con: system_prompt_fase + historial + mensaje_actual. Max tokens: 800. Respuesta esperada: JSON estructurado. |
| 8 | VALIDACIÓN JSON — Parsear respuesta. Si JSON inválido → Reintento automático (máx 2 veces). Si persiste → registrar error_json = TRUE → Paso 14 (HUMANO). |
| 9 | LÓGICA BACKEND (Make) — Calcular score_total sumando D1–D6. Clasificar nivel_riesgo. Determinar fase_siguiente. Activar flag_alarma si score ≥ 13 o D1 ≥ 2. |
| 10 | GOOGLE SHEETS — Actualizar PACIENTES: campos clínicos + fase_actual + nivel_riesgo + score_total + flag_alarma + ultima_actividad + version_prompt + version_flujo. |
| 11 | GOOGLE SHEETS — Insertar fila en CONVERSACIONES: conv_id, fase, mensaje_usuario, respuesta_agente, guia_soporte_turno, timestamp, tokens, flag_alarma, version_prompt. |
| 12 | ARRAY + JSON — Agregar turno al historial. Si >15 turnos → eliminar el más antiguo. Stringificar y actualizar historial_json en PACIENTES. |
| 13 | ROUTER — Si fase_siguiente = ADMIN → enviar link icnsalud.com/#contacto y cerrar flujo. |
| 14 | ROUTER — Si flag_alarma = TRUE o error_json persistente → Notificar al equipo ICN (nombre, teléfono, síntoma, fase, resumen). Registrar motivo_escalamiento. |
| 15 | ROUTER — Si F3 completada (fase_siguiente = F4) → Llamar Escenario 2 para enviar reporte estructurado de riesgo. |
| 16 | WHATSAPP — Enviar respuesta_visible al paciente. |

10. Filtro de Alarmas — Crítico (Antes de ChatGPT)

| Palabras clave / frases de alarma | Acción inmediata |
| --- | --- |
| Listado completo | convulsión / convulsiones · pérdida de conciencia / desmayo · no puedo mover (brazo/pierna/cara) · peor dolor de mi vida / de inicio súbito · rigidez de nuca / fiebre + cuello · pensamiento suicida / hacerme daño · cefalea en trueno · visión doble súbita · no puedo hablar de repente |
| Acción | 1. NO llamar a ChatGPT  \|  2. Activar flag_alarma = TRUE  \|  3. Notificar a neuroasesor interno ICN  \|  4. Enviar al paciente mensaje de orientación a urgencias + datos de contacto ICN  \|  5. Registrar motivo_escalamiento en Sheets |

11. Validación JSON y Fallback

| Caso | Acción de Make |
| --- | --- |
| JSON válido | Continuar flujo normal |
| JSON inválido — 1er fallo | Reintento automático (prompt: 'Responde SOLO JSON válido') |
| JSON inválido — 2do fallo | Segundo reintento automático |
| JSON inválido — 3er fallo | Registrar error_json = TRUE. Escalar a HUMANO. Enviar al paciente: 'En este momento un asesor te contactará.' |
| Paciente pide hablar con persona | fase_siguiente = HUMANO. Notificar a asesor ICN. |

DOCUMENTO 4 — PROMPTS (Versionados)

12. Sistema de Versiones

| Campo en Sheets | Descripción |
| --- | --- |
| version_prompt | Versión del prompt de fase activo en ese turno (ej: v5.0) |
| version_flujo | Versión de la lógica de flujo de Make activa (ej: v5.0) |

13. Formato JSON Obligatorio de Respuesta

| { "respuesta_visible": "Texto al paciente por WhatsApp", "notas_internas": "Solo visible para equipo ICN", "puntaje_dominio": {"D1": 2, "D2": 0, "D3": 3, "D4": 2, "D5": 2, "D6": 2}, "guia_soporte": "ICHD-3 criterio X / DSM-5-TR criterio Y", "cie10": "G43.009" } NOTA: nivel_riesgo, score_total, flag_alarma y fase_siguiente son calculados por Make. ChatGPT NO decide la fase siguiente. |
| --- |

14. Prompt Base del Sistema — v5.0

| SYSTEM PROMPT BASE — v5.0 Eres NeurOrientador, el sistema de teleorientación neurológica de ICN Salud. Tu rol es orientar a los pacientes mediante una evaluación estructurada de riesgo. Eres clínico, humano y orientador — siempre los tres a la vez. TONO OBLIGATORIO — TRÍADA: Clínico: transmites confianza y seriedad. El paciente sabe que está siendo orientado con rigor. Humano: transmites cercanía y calidez. Validas emocionalmente antes de avanzar en cualquier pregunta clínica. Comercial: orientas hacia la acción. Cuando es el momento correcto, facilitas el siguiente paso de forma natural, sin presión agresiva. REGLAS ABSOLUTAS (innegociables): Responde SIEMPRE en formato JSON válido (estructura definida). NUNCA emitas diagnóstico definitivo. Lenguaje obligatorio: 'Esto sugiere un nivel de riesgo…' / 'El especialista podrá confirmar…' NUNCA formules medicamentos ni recomiendes dosis. SIEMPRE indica en puntaje_dominio el valor numérico de cada dominio respondido. SIEMPRE presenta el servicio como teleorientación, no como consulta médica. Todos los pacientes deben pasar por F3 (teleorientación), sin excepción. Datos actuales del paciente: Nombre: {{nombre}}  \|  Edad: {{edad}}  \|  Ciudad: {{ciudad}}  \|  Aseguramiento: {{aseguramiento}}  \|  Fase: {{fase_actual}}  \|  Programa: {{programa_clinico}}  \|  Riesgo previo: {{nivel_riesgo}} |
| --- |

15. Mensajes / Copy del Sistema — Líneas de Referencia

El sistema debe producir mensajes que sigan las líneas de referencia definidas a continuación. Estas líneas no son guiones rígidos — son la referencia de tono, estructura y propósito que deben respetarse en todos los mensajes.

15.1 Mensaje Inicial (F0)

| Línea de referencia — Mensaje inicial Hola, bienvenido/a a ICN Salud 👋 Soy NeurOrientador, el sistema de orientación neurológica de ICN Salud. Estoy aquí para ayudarte a entender mejor lo que está pasando y orientarte hacia el paso más adecuado. ¿En qué te puedo ayudar hoy? Tono: cercano, claro, útil. No institucional frío. No menciona tecnicismos. Abre el espacio para que el paciente explique con sus palabras. |
| --- |

15.2 Consentimiento (F1)

| Línea de referencia — Consentimiento Antes de comenzar, necesito contarte tres cosas importantes: Tus datos están protegidos. Toda la información que compartas es confidencial y se trata según la Ley 1581 de 2012. Esto es una teleorientación, no una consulta médica. Lo que obtendrás es una evaluación de riesgo — no un diagnóstico. El especialista es quien confirma. Puedes usar este canal cuando necesites. Estamos disponibles las 24 horas, los 7 días de la semana. ¿Aceptas estos términos para continuar? Responde SÍ o NO. Tono: claro, corto, comprensible. Sin fricción innecesaria. Tres puntos concretos, no un bloque de texto legal. |
| --- |

15.3 F3 — Teleorientación

| Principios de copy para F3 Preguntas cortas: Una o dos preguntas por turno. Nunca listas largas. Validación emocional primero: Antes de la siguiente pregunta, validar brevemente lo que el paciente acaba de decir. ('Entiendo que eso ha sido muy difícil…', 'Gracias por contarme, eso me ayuda mucho a orientarte mejor.') Claridad: Sin tecnicismos. Si se usa un término clínico, se explica de inmediato en lenguaje sencillo. Sensación de guía: El paciente debe sentir que está siendo llevado por alguien que sabe lo que hace, no que está llenando un formulario. Ejemplo de turno F3: 'Gracias por contarme eso — 3 o 4 veces a la semana durante 3 meses es bastante y entiendo que debe ser agotador. Ahora dime: del 0 al 10, ¿qué tanto te afectan estos dolores en tu día a día — en el trabajo, en casa, en tu descanso?' |
| --- |

15.4 F4 — Conversión

| Principios de copy para F4 Siempre se orienta a cierre: No se deja la conversación abierta ni en espera. Cada turno de F4 avanza hacia la agenda. Siempre se ofrecen horarios concretos: '¿Te queda mejor el jueves o el viernes?' — nunca '¿Te gustaría agendar?' Sin preguntas abiertas de cierre: '¿Quieres agendar?' es una pregunta que invita a decir que no. Reemplazarla siempre por opciones concretas. Tono que invita sin presionar: El cierre debe sentirse como el paso natural y lógico, no como una venta a presión. Ejemplo de turno de cierre F4: 'Con base en lo que me contaste, llevas varios meses con estos dolores que ya te están afectando en el trabajo — y eso es exactamente lo que el neurólogo puede ayudarte a resolver. Tenemos disponibilidad esta semana. ¿Te queda mejor el jueves en la mañana o el viernes en la tarde?' |
| --- |

15.5 NeuroAsistente — Mensajes de Acompañamiento

| Principios de copy para NeuroAsistente Cercanos: El mensaje no suena a notificación automática. Suena a alguien que de verdad está pendiente. Tranquilos: No generan ansiedad ni urgencia innecesaria. El tono es sereno y confiable. Disponibles: Siempre incluyen la idea de que el paciente puede escribir cuando lo necesite. Útiles: Cada mensaje tiene un propósito claro: confirmar, preparar, recordar o saber cómo le fue. Con acompañamiento real: El paciente siente que hay un sistema — y un equipo — que lo sigue. Ejemplo — Mensaje de seguimiento post consulta (1 día después): 'Hola [nombre] 👋 ¿Cómo te fue ayer en tu consulta con el neurólogo? Queremos saber cómo estás y si quedaste con alguna duda o necesitas ayuda con algo. Estamos aquí para acompañarte — puedes escribirnos cuando lo necesites.' |
| --- |

DOCUMENTO 5 — PROMPTS POR FASE v5.0

16. Prompt F0 — Clasificación Inicial

| PROMPT F0 — v5.0 {{SYSTEM_PROMPT_BASE}} FASE: F0 — Clasificar intención del primer mensaje. REGLAS DE CLASIFICACIÓN: Síntomas / interés clínico / precio / cita → notas_internas: tipo=teleorientacion EPS / autorización / historia clínica / admin → notas_internas: tipo=admin (respuesta_visible incluye link icnsalud.com/#contacto) Prepagada / particular → notas_internas: tipo=teleorientacion En respuesta_visible: saludo breve, cercano, útil. Ni frío ni excesivamente informal. Make determina la fase_siguiente según notas_internas. |
| --- |

17. Prompt F1 — Consentimiento e Identificación

| PROMPT F1 — v5.0 {{SYSTEM_PROMPT_BASE}} FASE: F1 — Consentimiento informado + datos básicos. PASO 1 — Si consentimiento_datos_clinicos = FALSE: Enviar mensaje de consentimiento en el tono de la línea de referencia 15.2: claro, corto, sin fricción. Incluir los tres puntos: protección de datos (Ley 1581/2012), naturaleza del servicio (teleorientación, no consulta), disponibilidad 24/7. Solicitar los tres consentimientos por separado: A. datos clínicos, B. términos de teleorientación, C. investigación (opcional). Si A = NO o B = NO → no puede continuar el flujo → icnsalud.com/#contacto. Si C = NO → continúa la atención, no entra en cohorte de investigación. PASO 2 — Capturar: nombre, edad, ciudad, aseguramiento. MÁXIMO 2 preguntas por turno. NO hacer preguntas clínicas aquí. PASO 3 — Si datos completos: mostrar programas disponibles. Make determina fase_siguiente = F2. |
| --- |

18. Prompt F2 — Selección de Problema Neurológico

| PROMPT F2 — v5.0 {{SYSTEM_PROMPT_BASE}} FASE: F2 — Seleccionar problema neurológico y confirmar ruta F3. REGLA: Todos los pacientes pasan por F3. Si el paciente pide precio o cita: explicar que primero se hace la evaluación de riesgo. 10 PROBLEMAS DISPONIBLES: 1. Dolor de cabeza  2. Convulsiones  3. Retraso en neurodesarrollo  4. Temblores y movimientos anormales  5. Problemas de sueño  6. Problemas de memoria  7. ACV  8. Parálisis facial  9. Dolores crónicos  10. Problemas neuromusculares Si el paciente menciona múltiples problemas: 'Podemos evaluar un problema por teleconsulta. ¿Cuál le afecta más hoy?' Anotar otros en notas_internas. Si detectas riesgo de autolesión, crisis emocional severa o agotamiento extremo: requiere_escalamiento_humano=TRUE. Make escala a HUMANO. No continuar a F3. |
| --- |

19. Prompt F3 — Teleorientación Neurológica — v5.0

| PROMPT F3 — v5.0 (Ejemplo: Cefalea / ICHD-3) {{SYSTEM_PROMPT_BASE}} FASE: F3 — Teleorientación neurológica estructurada. Programa: {{programa_clinico}}  \|  Problema: {{problema_seleccionado}}  \|  Guía base: ICHD-3 (Cefalea) REGLA DE CIERRE ANTICIPADO (NUEVA EN V5): F3 no debe volverse rígida ni excesivamente larga. Si con la información disponible ya es posible orientar clínicamente al paciente con suficiente claridad, la evaluación puede cerrarse antes de agotar todos los dominios. No es obligatorio recorrer mecánicamente D1–D6 si el caso ya está suficientemente orientado. El objetivo es la orientación clínica útil, no la exhaustividad formal. ÁRBOL CONVERSACIONAL — 6 DOMINIOS (máximo 5–6 turnos, 2 preguntas/turno, con posibilidad de cierre anticipado): D1 BANDERAS ROJAS (prioridad 1 — siempre primero): '¿Ha tenido fiebre, vómito en proyectil, visión doble, pérdida de fuerza, el peor dolor de su vida de inicio súbito, rigidez en la nuca?' Puntaje D1: ninguno = 0 \| uno = 1 \| dos o más = 3 (flag inmediato en notas_internas) D2 CARACTERIZACIÓN (ICHD-3 Criterio A): '¿Cuántas veces por semana/mes? ¿Desde hace cuánto tiempo?' Puntaje D2: <1/sem = 1 \| 1-2/sem = 2 \| ≥3/sem o crónico = 3 D3 TIPO Y LOCALIZACIÓN (ICHD-3 Criterio B): '¿El dolor es pulsátil o en presión? ¿En qué zona?' Puntaje D3: pulsátil unilateral = 2 \| bilateral/presión = 1 \| otro = 0 D4 SEVERIDAD (ICHD-3 Criterio C): '¿Del 0 al 10 cuánto le afecta en su vida diaria?' Puntaje D4: 1-4 = 1 \| 5-7 = 2 \| 8-10 = 3 D5 FENOTIPO (ICHD-3 Criterio C): '¿Sensibilidad a luz, ruido, náuseas, aura visual?' Puntaje D5: uno = 1 \| dos = 2 \| tres o más = 3 D6 HISTORIAL (tratamiento y respuesta): '¿Ha tomado medicamento? ¿Con qué resultado?' Puntaje D6: sin medicamento/sin efecto = 3 \| efecto parcial = 2 \| buen control = 1 IMPORTANTE: Solo indica los puntajes en puntaje_dominio. Make calcula el score_total, nivel_riesgo y fase_siguiente. En respuesta_visible: SIEMPRE lenguaje de teleorientación — 'Esto sugiere un nivel de riesgo…' / 'El especialista podrá confirmar…' NUNCA: 'Tienes X' / 'Tu diagnóstico es X'. |
| --- |

20. Prompt F4 — Conversión Clínica — v5.0

| PROMPT F4 — v5.0 {{SYSTEM_PROMPT_BASE}} FASE: F4 — Conversión clínica. Esta es la fase de cierre. Cada turno debe avanzar hacia la agenda. Riesgo: {{nivel_riesgo}}  \|  Fenotipo: {{fenotipo_probable}}  \|  CIE-10: {{cie10}} ESTRUCTURA OBLIGATORIA DE F4: T1 — Resultado clínico: Resumir hallazgos con lenguaje prudente y clínico. Anclar la propuesta en los datos del paciente. T2 — Consecuencia: Explicar brevemente por qué vale la pena actuar. No alarmar, pero sí dar contexto real. T3 — Propuesta concreta: Presentar el paquete o consulta del programa. Qué incluye, qué resuelve. T4 — Cierre directo: Ofrecer horarios concretos. NUNCA preguntar '¿quieres agendar?'. SÍ usar: '¿Te queda mejor el jueves o el viernes?' MANEJO DE OBJECIONES: 'Es caro' → Costo de tratamiento tardío vs. valor del diagnóstico temprano. 'Ya fui al médico' → Valor del neurólogo especialista vs. médico general. 'Tengo miedo' → Validar, normalizar, enfocar en solución. 'Quiero pensarlo' → Respetar, ofrecer información adicional, acordar seguimiento concreto. 'Soy EPS' → Redirigir a icnsalud.com/#contacto. ESCALAMIENTO COMERCIAL — OBLIGATORIO: Si el paciente: (a) duda de forma repetida, (b) pregunta reiteradamente por precio sin avanzar, (c) no decide después de 3 turnos de F4, o (d) pide hablar con alguien → escalar a NeuroAsesor comercial. Al escalar, Make envía al equipo ICN: nombre · teléfono · problema principal · nivel de riesgo · resumen clínico · motivo del escalamiento. Indicar en notas_internas: requiere_neuroasesor_comercial=TRUE + motivo. |
| --- |

DOCUMENTO 6 — NEUROASISTENTE: ACOMPAÑAMIENTO, TRAZABILIDAD Y RETROALIMENTACIÓN

21. Rol y Principio del NeuroAsistente

| PRINCIPIO FUNDAMENTAL DEL NEUROASISTENTE El NeuroAsistente no opera como una capa invisible. Todo contacto con el paciente queda registrado, trazado y disponible para revisión. Su objetivo no es solo operar — es aprender, mejorar y hacer que el paciente se sienta acompañado en todo momento. El NeuroAsistente se activa automáticamente cuando un paciente agenda una cita y acompaña desde ese momento hasta el día después de la consulta. |
| --- |

22. Flujo de Acompañamiento Definitivo

Cuando un paciente agenda una cita, Make activa automáticamente el flujo de acompañamiento del NeuroAsistente. La secuencia es:

| Paso | Tipo de interacción | Descripción y objetivo |
| --- | --- | --- |
| 1 | confirmacion_cita | Confirmar que la cita quedó agendada correctamente. Dar al paciente la información básica (fecha, hora, modalidad). Reforzar que puede escribir si necesita algo. |
| 2 | preparacion_cita | Enviar instrucciones de preparación (si aplica para el programa): qué llevar, si hay ayuno, cómo llegar o conectarse. Responder dudas logísticas. |
| 3 | recordatorio | Recordatorio 1 día antes de la cita. Tono cálido, no de notificación automática. Incluir datos clave de la cita. Invitar a confirmar asistencia. |
| 4 | seguimiento_post_cita | 1 DÍA DESPUÉS de la cita: preguntar cómo le fue, si entendió todo, si necesita ayuda, reforzar que puede escribir cuando lo necesite. |

| SEGUIMIENTO POST CONSULTA — REGLA OPERATIVA V5 El seguimiento post consulta se realiza exactamente 1 día después de la fecha de la cita, no antes. Objetivo del seguimiento post consulta: Preguntar cómo le fue en la consulta Verificar si entendió todo lo que le explicaron Preguntar si necesita ayuda con algo (dudas, indicaciones, próximos pasos) Reforzar que puede escribirnos cuando necesite Mantener la percepción de acompañamiento continuo por parte de ICN Salud |
| --- |

23. Tipos de Interacción del NeuroAsistente

| Tipo de interacción | Descripción y posible escalamiento |
| --- | --- |
| confirmacion_cita | Confirma agenda. Escalamiento comercial si cancela. |
| preparacion_cita | Envía instrucciones de preparación. Escalamiento clínico si hay duda médica. |
| recordatorio | Recordatorio 1 día antes. Escalamiento comercial si no responde. |
| seguimiento_post_cita | 1 día después de la consulta. Escalamiento clínico si hay complicación o duda médica; comercial si hay interés en nueva consulta o cancelación sin reagendar. |
| resolucion_duda | Respuesta a pregunta sobre el proceso o la cita. Escalamiento clínico si es duda médica. |
| acompañamiento | Mensaje de apoyo ante señal emocional o vulnerabilidad. Escalamiento clínico si hay riesgo. |
| oportunidad_comercial | Detección de interés en nuevo programa o consulta adicional. Escalamiento comercial. |

24. Lógica de Escalamiento desde NeuroAsistente

| Señal detectada en respuesta del paciente | Rev. clínica | Rev. comercial | Acción generada |
| --- | --- | --- | --- |
| Complicación clínica post consulta (dolor, reacción, síntoma nuevo) | TRUE | FALSE | Notificar equipo médico ICN → escalado_clinico |
| Duda sobre medicamento recetado | TRUE | FALSE | Escalar a neuroasesor clínico. No responder directamente. |
| Señal emocional o angustia expresada | TRUE | FALSE | Escalar a HUMANO (neuroasesor). Registrar en notas_internas. |
| Inconformidad con el servicio | FALSE | TRUE | Notificar asesor comercial → escalado_comercial |
| Interés en nuevo programa o consulta adicional | FALSE | TRUE | Registrar oportunidad. Notificar asesor comercial. |
| Cancelación de cita sin reagendar | FALSE | TRUE | Notificar asesor comercial para seguimiento. |
| Respuesta normal / confirmación | FALSE |  | accion_generada = ninguna. Estado = cerrado. |

25. Escalamiento Comercial — Información Obligatoria al Equipo

| PROTOCOLO DE ESCALAMIENTO COMERCIAL Cuando se activa un escalamiento a NeuroAsesor comercial — ya sea desde F4 o desde el NeuroAsistente — Make debe enviar al equipo interno de ICN la siguiente información de forma obligatoria: Nombre del paciente Teléfono de contacto Problema principal identificado en F2/F3 Nivel de riesgo calculado por Make (Bajo / Moderado / Alto / Alarma) Resumen clínico (notas_internas de F3) Motivo del escalamiento (duda repetida / pregunta de precio / no decide / pide hablar / cancela / interés nuevo programa) |
| --- |

26. Flujo de Registro en Make — Escenario NeuroAsistente

| Paso | Acción en Make |
| --- | --- |
| 1 | TRIGGER — El NeuroAsistente se activa por: schedule de cita, evento de confirmación de agenda, o mensaje entrante del paciente relacionado con una cita activa. |
| 2 | GOOGLE SHEETS — Recuperar datos del paciente (paciente_id, nombre, cita_id, programa_clinico, fase_actual, prioridad_operativa, historial reciente). |
| 3 | ChatGPT API (opcional) — Si la interacción requiere lenguaje personalizado (seguimiento post cita), generar mensaje con contexto del paciente y tono de la tríada. Si es recordatorio estándar, usar plantilla fija. |
| 4 | WHATSAPP — Enviar mensaje al paciente. Registrar timestamp exacto. |
| 5 | GOOGLE SHEETS — Insertar fila en NEUROASISTENTE_INTERACCIONES con todos los campos obligatorios (ver sección 27). |
| 6 | ESPERAR RESPUESTA — Cuando el paciente responde, Make detecta el mensaje y lo asocia al interaccion_id por paciente_id + cita_id + estado=enviado más reciente. |
| 7 | ANÁLISIS DE RESPUESTA — Make + ChatGPT evalúan el contenido: determinar requiere_revision_clinica y requiere_revision_comercial. |
| 8 | GOOGLE SHEETS — Actualizar fila en NEUROASISTENTE_INTERACCIONES: respuesta_paciente, estado, flags, accion_generada, timestamp_actualizacion. |
| 9 | ROUTER — Si requiere_revision_clinica = TRUE: notificar equipo médico ICN. Si requiere_revision_comercial = TRUE: notificar asesor comercial con información completa del protocolo de escalamiento. |
| 10 | Sin respuesta en 24h: estado = pendiente. Sin respuesta en 48h adicionales: estado = cerrado + notas_internas = 'sin respuesta tras 2 intentos'. |

DOCUMENTO 7 — MODELO DE DATOS

27. NEUROASISTENTE_INTERACCIONES — Esquema Completo (V5)

| TRAZABILIDAD TOTAL — REGLA OPERATIVA NO NEGOCIABLE Todo lo que haga el NeuroAsistente debe quedar registrado en la hoja NEUROASISTENTE_INTERACCIONES. Esto no es opcional. Es obligatorio para la trazabilidad, la auditoría y la retroalimentación del sistema. |
| --- |

| Campo | Tipo | Descripción y reglas de validación |
| --- | --- | --- |
| interaccion_id | Texto (auto) | ID único. Formato: NA-{paciente_id}-{YYYYMMDDTHHmmss}. Único y ordenable cronológicamente. |
| paciente_id | Texto | FK → PACIENTES. Obligatorio. Validar existencia antes de insertar. |
| cita_id | Texto | FK → CITAS. Obligatorio si está relacionado con una cita. Puede quedar vacío en acompañamiento general. |
| fecha_hora | Fecha-hora | Timestamp exacto del momento en que el NeuroAsistente envía el mensaje. ISO 8601. Generado automáticamente. |
| canal_contacto | Texto | Canal utilizado. Valores: WhatsApp \| Email \| SMS. En MVP: siempre WhatsApp. |
| tipo_interaccion | Texto | Valores: confirmacion_cita \| preparacion_cita \| recordatorio \| seguimiento_post_cita \| resolucion_duda \| acompañamiento \| oportunidad_comercial |
| mensaje_enviado | Texto | Texto completo del mensaje enviado al paciente. Obligatorio. |
| respuesta_paciente | Texto | Respuesta exacta del paciente. Si no responde en 24h: registrar 'sin_respuesta'. Actualizar si responde después. |
| estado_interaccion | Texto | Valores: enviado \| respondido \| pendiente \| cerrado \| escalado |
| requiere_revision_clinica | Booleano | TRUE si la respuesta contiene señal clínica. Activa revisión por equipo médico ICN. |
| requiere_revision_comercial | Booleano | TRUE si la respuesta contiene señal comercial. Activa seguimiento por asesor comercial. |
| notas_internas | Texto | Observaciones del NeuroAsistente o equipo ICN. Solo visible internamente. No se comparte con el paciente. |
| responsable | Texto | Valores: NeuroAsistente_automatico \| Neuroasesor_humano \| Sistema_Make |
| accion_generada | Texto | Valores: ninguna \| cita_confirmada \| cita_reprogramada \| escalado_clinico \| escalado_comercial \| nueva_teleconsulta_agendada |
| prioridad_paciente | Texto | Nivel de prioridad operativa del paciente: agendado \| particular \| general |
| version_flujo | Texto | Versión del flujo del NeuroAsistente activo. Ejemplo: v5.0 |
| timestamp_actualizacion | Fecha-hora | Última actualización del registro (cuando el paciente responde, cambia estado, etc.). |

28. Retroalimentación del Sistema — Uso Analítico de los Datos

El objetivo de registrar todas las interacciones del NeuroAsistente no es solo la auditoría operativa. Es también la retroalimentación continua del sistema para que mejore con el tiempo.

| USO ANALÍTICO — CAMPOS CLAVE Y PREGUNTAS QUE RESPONDEN tipo_interaccion + estado_interaccion → ¿Qué tipos de contacto generan más respuesta del paciente? → Optimizar cuándo y cómo contactar. respuesta_paciente (texto libre) → ¿Qué dudas y preocupaciones expresan los pacientes? → Identificar patrones frecuentes. requiere_revision_clinica / comercial → ¿Qué porcentaje de interacciones escala? → Ajustar umbrales y reducir carga del equipo humano. accion_generada + conversion (PACIENTES) → ¿Qué mensajes generan mayor conversión o reconsulta? → A/B testing de mensajes. fecha_hora + estado=sin_respuesta → ¿En qué horarios hay menor tasa de respuesta? → Ajustar ventanas de contacto. version_flujo + tasa de escalamiento → ¿Las nuevas versiones del NeuroAsistente reducen errores? → Comparar versiones y validar mejoras antes de producción. seguimiento_post_cita + resultado_post (CITAS) → ¿El acompañamiento post cita mejora la adherencia al tratamiento? → Medir impacto real del NeuroAsistente. |
| --- |

29. Relaciones entre Hojas del Sistema

| PACIENTES (1) ─────── (N) NEUROASISTENTE_INTERACCIONES CITAS (1) ─────────── (N) NEUROASISTENTE_INTERACCIONES CONVERSACIONES ──── historial previo (evitar mensajes repetitivos) Campos de lectura cruzada recomendados: PACIENTES.nivel_riesgo → contexto clínico para personalizar mensajes PACIENTES.programa_clinico → adaptar tono y contenido según programa PACIENTES.prioridad_operativa → aplicar orden de prioridad en seguimiento CITAS.fecha_cita + CITAS.confirmacion → determinar tipo de interacción activa CITAS.resultado_post → base para seguimiento post consulta (1 día después) |
| --- |

DOCUMENTO 8 — ESCALAMIENTO HUMANO Y COMERCIAL

30. Escalamiento Clínico — Obligatorio

| Trigger | Descripción | Acción |
| --- | --- | --- |
| Filtro de alarma (pre-ChatGPT) | Palabras clave detectadas en mensaje bruto del paciente | NO llamar a ChatGPT. Activar flag_alarma. Notificar neuroasesor. Orientar a urgencias si aplica. |
| flag_alarma en D1 (F3) | Score D1 = 2 o más banderas rojas en árbol clínico | fase_siguiente = HUMANO. Notificar neuroasesor con resumen clínico. |
| Error JSON persistente | JSON inválido después de 2 reintentos | Registrar error_json = TRUE. Escalar a HUMANO. Mensaje de espera al paciente. |
| Señal emocional fuerte (F2) | Riesgo de autolesión o crisis severa detectada | fase_siguiente = HUMANO inmediatamente. |
| Solicitud del paciente | Paciente pide hablar con una persona | fase_siguiente = HUMANO. Notificar asesor ICN. |
| EPS detectada | Paciente es usuario de EPS | fase_siguiente = ADMIN. Redirigir a icnsalud.com/#contacto. |
| Duda clínica del sistema | IA no puede clasificar con certeza | Registrar motivo_escalamiento. fase_siguiente = HUMANO. |

31. Escalamiento Comercial — Definición Formal

El escalamiento comercial es una ruta formal del sistema — no una observación. Ocurre cuando la conversación supera la capacidad del flujo automático para convertir y requiere intervención humana del equipo comercial de ICN Salud.

| Trigger de escalamiento comercial | Información que se envía al equipo ICN |
| --- | --- |
| F4: paciente duda de forma repetida (3+ turnos sin decidir) | Nombre, teléfono, problema principal, nivel de riesgo, resumen clínico, motivo del escalamiento |
| F4: pregunta repetida por precio sin avanzar | Ídem |
| F4: paciente pide hablar con alguien | Ídem |
| NeuroAsistente: cancelación sin reagendar | Nombre, teléfono, cita_id, fecha original, motivo si fue expresado |
| NeuroAsistente: interés en nuevo programa o reconsulta | Nombre, teléfono, programa de interés, nivel de riesgo, contexto |
| NeuroAsistente: inconformidad con el servicio | Nombre, teléfono, descripción de la inconformidad |

32. Resumen de Decisiones V5 — Referencia Rápida

| CAMBIOS OPERATIVOS INTEGRADOS EN V5 Seguimiento post consulta: 1 día después de la cita (no 2 horas). Disponibilidad: 24 horas al día, 7 días a la semana. NeurOrientador y NeuroAsistente. Prioridad operativa: 1. Agendados → 2. Particulares → 3. Resto. Tono: Tríada obligatoria — Clínico + Humano + Comercial en todo mensaje. F3: Cierre anticipado permitido si ya hay suficiente información clínica. No es obligatorio agotar todos los dominios. F4: Fase de conversión explícita. Cierre con horarios concretos. Sin preguntas abiertas. Escalamiento comercial formal. NeuroAsistente: Flujo formal: confirmación → preparación → recordatorio → seguimiento (1 día después). Trazabilidad: Todo lo que haga el NeuroAsistente se registra. Obligatorio. No opcional. Retroalimentación: Los datos del NeuroAsistente permiten aprender qué mensajes funcionan, qué dudas aparecen y qué interacciones derivan en conversión. Volumen inicial: ~500 pacientes. Sin límite rígido de mensajes. |
| --- |



---

# FUENTE V4.1: NeurOrientador_V4_1 (2).docx

**Rol de esta fuente:** MVP + NeuroAsistente; útil para trazabilidad y decisiones pospuestas.


NeurOrientador

ICN Salud — Sistema Clínico de Teleorientación Neurológica

| Documentación Técnica de Implementación — Versión 4.1  (MVP + NeuroAsistente) Stack: WhatsApp Business API  ·  Make  ·  ChatGPT API (GPT-4o)  ·  Google Sheets Base metodológica: ICHD-3  ·  DSM-5-TR  ·  Guías ICN  ·  Modelo UNI de Evaluación de Riesgo 2026 |
| --- |

| 📋 NOTA DE VERSIÓN:  Esta versión 4.1 incorpora el módulo completo del NeuroAsistente.V4.0: Ajuste de alcance MVP (F0–F4), separación de lógica clínica, control de consentimientos.V4.1: Agrega Documento 5 — Trazabilidad y Registro del NeuroAsistente (hoja NEUROASISTENTE_INTERACCIONES).Fases implementadas: F0 · F1 · F2 · F3 · F4 + NeuroAsistenteFases pospuestas: F5 · F6 · ESRI · Investigación avanzada · Cohortes complejas |
| --- |

DOCUMENTO 1 — ALCANCE MVP

| DOCUMENTO 1 — ALCANCE MVP |
| --- |

1. Objetivo del MVP

El MVP de NeurOrientador debe cumplir un objetivo claro y específico:

| 🎯 OBJETIVO DEL MVP Un sistema que: recibe pacientes · hace teleorientación · clasifica riesgo · genera confianza · convierte a cita |
| --- |

2. Fases del MVP — Qué Entra y Qué No Entra

| ✅ INCLUIDO EN MVP | 🚫 EXCLUIDO DEL MVP |
| --- | --- |
| F0 — Clasificación inicial F1 — Consentimiento e identificación F2 — Selección de problema neurológico F3 — Teleorientación clínica (scoring) F4 — Conversión a cita | F5 — Seguimiento automático de citas F6 — Educación recurrente preventiva ESRI — Contexto geográfico/socioeconómico Automatización de investigación avanzada Lógica compleja de cohortes Modelos predictivos Optimización avanzada de conversión |

| ⚠️ REGLA FUNDAMENTAL (no negociable): Todo paciente debe completar F3 antes de agendar.No se puede saltar F3 aunque el paciente llegue preguntando por precio o cita directamente.Una teleconsulta = un problema neurológico. Si hay múltiples, se agenda una teleconsulta separada para cada uno. |
| --- |

3. Decisiones de Diseño Críticas

3.1 Lógica clínica separada de ChatGPT

La lógica crítica del sistema NO puede residir solo en prompts de IA. Se separa de la siguiente forma:

| RESPONSABILIDAD DE MAKE (backend) | RESPONSABILIDAD DE ChatGPT (IA) |
| --- | --- |
| Cálculo de score_total (suma D1–D6) Clasificación de nivel_riesgo Activación de flag_alarma Transición de fases (F3→F4 / HUMANO) Validación del JSON de respuesta Filtro de palabras clave de alarma | Generación de preguntas conversacionales Lenguaje empático y adaptado respuesta_visible (texto al paciente) notas_internas (síntesis clínica) Adaptación de tono por contexto |

3.2 F2.5 (Evaluación Psicosocial) — Simplificada para MVP

Para el MVP, F2.5 se simplifica a detección básica de señales emocionales fuertes.

| Condición | Acción en MVP |
| --- | --- |
| Sin señales emocionales | Flujo directo F2 → F3. Sin evaluación psicosocial. |
| Señales emocionales leves | Continuar a F3 con mayor empatía en el tono conversacional. |
| Señales emocionales fuertes o riesgo de autolesión | Escalar directamente a HUMANO. No continuar flujo automático. |

| 📌 POSPUESTO para V2: La evaluación completa de APGAR + Ecomapa + Hamilton queda pospuesta para V2.No incluir en MVP. |
| --- |

3.3 Reporte Visual de Riesgo — Simplificado para MVP

Para el MVP se utiliza un mensaje estructurado de texto enriquecido por WhatsApp en lugar de imagen generada.

| MVP (Implementar ahora) | V2 (Posponer) |
| --- | --- |
| Mensaje WhatsApp estructurado con: nombre, programa, nivel de riesgo, fenotipo, recomendación, disclaimer legal Formato de texto simple, sin imagen externa Disclaimer legal SIEMPRE incluido en el texto | Imagen generada con Bannerbear, hcti.io o HTML-to-image Branding visual con logo ICN Escenario Make separado para generación de imagen |

3.4 Dashboard del Neurólogo — MVP

No se requiere sistema complejo. En MVP se utiliza Google Sheets con filtros básicos.

| El equipo clínico puede ver en Sheets: |
| --- |
| • Nombre del paciente y datos básicos |
| • Nivel de riesgo (Bajo / Moderado / Alto / Alarma) |
| • Fenotipo probable y código CIE-10 |
| • Síntomas clave (respuestas_orientacion en JSON) |
| • Resumen clínico (notas_internas) |
| • Estado de la cita y motivo de escalamiento |

3.5 Lenguaje del Sistema — Ajuste Obligatorio

Se modifica el lenguaje en toda la documentación y en los prompts:

| ❌ LENGUAJE ANTERIOR (eliminar) | ✅ LENGUAJE CORRECTO (usar) |
| --- | --- |
| 'evidencia clínica validada' | 'base inicial para análisis clínico' |
| 'base de investigación consolidada' | 'datos estructurados para futura validación' |
| 'sistema clínico validado' | 'herramienta de orientación en etapa inicial' |

| DOCUMENTO 2 — FLUJOS MAKE |
| --- |

4. Escenarios Make — MVP

El MVP opera con 2 escenarios activos. Los escenarios de F5 y F6 quedan pospuestos.

| Escenario | Propósito | Trigger | Estado MVP |
| --- | --- | --- | --- |
| Escenario 1 | Conversación principal (F0–F4) | Webhook permanente WhatsApp | ✅ Activo |
| Escenario 2 | Notificación estructurada de riesgo al cierre de F3 | Llamada desde Escenario 1 | ✅ Activo (texto, no imagen) |
| Escenario 3 | Recordatorios F5 (seguimiento citas) | Programado diario 8am | 🚫 Pospuesto V2 |
| Escenario 4 | Seguimiento preventivo F6 (educación) | Programado Lun/Mié/Vie 9am | 🚫 Pospuesto V2 |

4.1 Escenario 1 — Conversación Principal (Detallado)

| TRIGGER: Webhook HTTP ← WhatsApp Business API \| Activo 24/7 |
| --- |

| Paso | Acción en Make |
| --- | --- |
| 1 | WEBHOOK — Recibir mensaje. Parsear: numero_telefono, mensaje_texto, timestamp. Verificar firma HMAC. |
| 2 | FILTRO ALARMA (ANTES de ChatGPT) — Buscar palabras clave en el mensaje bruto: 'convulsión', 'pérdida de conciencia', 'no puedo mover', 'peor dolor de mi vida', 'rigidez de nuca', 'pensamiento suicida'. Si se detecta → IR A PASO 14 DIRECTO (NO llamar ChatGPT). |
| 3 | GOOGLE SHEETS — Buscar paciente por teléfono (clave primaria). Si no existe → Paso 4a. Si existe → Paso 4b. |
| 4a | GOOGLE SHEETS — Crear nuevo paciente: telefono, fecha_creacion, fase_actual=F0, historial_json=[], consentimientos=FALSE. |
| 4b | GOOGLE SHEETS — Leer datos del paciente: fase_actual, historial_json, programa_clinico, nivel_riesgo, nombre, consentimientos, version_prompt, version_flujo. |
| 5 | JSON PARSE — Deserializar historial_json (string → array). Truncar a máximo 15–20 turnos (eliminar los más antiguos si supera el límite). |
| 6 | ROUTER — Seleccionar system prompt por fase_actual (F0, F1, F2, F3, F4, ADMIN, HUMANO). Registrar version_prompt y version_flujo activos. |
| 7 | ChatGPT API (GPT-4o) — Llamar con: system_prompt_fase + historial + mensaje_actual. Max tokens: 800. Respuesta esperada: JSON estructurado. |
| 8 | VALIDACIÓN JSON — Parsear respuesta. Si JSON inválido → Reintento automático (máx 2 veces). Si persiste error → registrar error_json = TRUE → Paso 14 (HUMANO). |
| 9 | LÓGICA BACKEND (Make) — Calcular score_total sumando puntajes D1–D6 según tabla de scoring. Clasificar nivel_riesgo según umbrales. Determinar fase_siguiente. Activar flag_alarma si score ≥ 13 o dominio D2 ≥ 2. |
| 10 | GOOGLE SHEETS — Actualizar PACIENTES: campos_actualizar + fase_actual + nivel_riesgo + score_total + flag_alarma + ultima_actividad + version_prompt + version_flujo. |
| 11 | GOOGLE SHEETS — Insertar fila en CONVERSACIONES: conv_id, fase, mensaje_usuario, respuesta_agente, guia_soporte_turno, timestamp, tokens, flag_alarma, version_prompt. |
| 12 | ARRAY + JSON — Agregar turno al historial. Si >15 turnos → eliminar el más antiguo. Stringificar. Actualizar historial_json en PACIENTES. |
| 13 | ROUTER — Si fase_siguiente = ADMIN → enviar link https://icnsalud.com/#contacto y cerrar flujo. |
| 14 | ROUTER — Si flag_alarma = TRUE o error_json persistente → Notificar al número interno ICN (nombre, teléfono, síntoma, fase, resumen). Registrar motivo_escalamiento. |
| 15 | ROUTER — Si F3 completada (fase_siguiente = F4) → Llamar Escenario 2 para enviar reporte estructurado de riesgo. |
| 16 | WHATSAPP — Enviar respuesta_visible al paciente. |

4.2 Escenario 2 — Reporte Estructurado de Riesgo (MVP)

| TRIGGER: Llamada desde Escenario 1 al completar F3 |
| --- |

| Paso | Acción |
| --- | --- |
| 1 | Recibir parámetros: nombre, nivel_riesgo, fenotipo_probable, programa_clinico, guia_soporte, cie10. |
| 2 | Construir mensaje estructurado WhatsApp con los datos del paciente y el disclaimer legal completo. |
| 3 | WHATSAPP — Enviar el mensaje estructurado al paciente. Incluye: nivel de riesgo, fenotipo probable, recomendación y disclaimer legal (texto obligatorio). |
| 4 | GOOGLE SHEETS — Actualizar reporte_enviado = TRUE + timestamp_reporte. |
| 5 | GOOGLE SHEETS — Si consentimiento_investigacion = TRUE: insertar fila anonimizada en COHORTES_INVESTIGACION. Si FALSE: no insertar datos. |

| 📋 Formato del mensaje de reporte (MVP):📋 EVALUACIÓN DE RIESGO NEUROLÓGICO — ICN SaludPaciente: [nombre] \| Fecha: [fecha]Programa evaluado: [programa_clinico]Nivel de riesgo: [ALTO/MODERADO/BAJO]Fenotipo probable: [fenotipo]Guía de referencia: [guia_soporte]Recomendación: Evaluación con especialista neurólogo.⚠️ AVISO: Este resultado corresponde a una evaluación de riesgo y NO constituye un diagnóstico médico. No reemplaza la consulta con un especialista. |
| --- |

4.3 Filtro de Alarmas (CRÍTICO — Antes de ChatGPT)

Este filtro se implementa en Make ANTES de llamar a ChatGPT. Es obligatorio y no negociable.

| Palabras clave / frases de alarma | Acción inmediata |
| --- | --- |
| convulsión / convulsiones pérdida de conciencia / desmayo no puedo mover (brazo/pierna/cara) peor dolor de mi vida / de inicio súbito rigidez de nuca / fiebre + cuello pensamiento suicida / hacerme daño cefalea en trueno visión doble súbita no puedo hablar de repente | 1. NO llamar a ChatGPT 2. Activar flag_alarma = TRUE 3. Notificar a neuroasesor interno ICN 4. Enviar al paciente: mensaje de orientación a urgencias + datos de contacto ICN 5. Registrar motivo_escalamiento en Sheets |

4.4 Validación JSON y Fallback Obligatorio

| Caso | Acción de Make |
| --- | --- |
| JSON válido en primer intento | Continuar flujo normal |
| JSON inválido — 1er fallo | Reintento automático (prompt de corrección: 'Responde SOLO JSON válido') |
| JSON inválido — 2do fallo | Segundo reintento automático |
| JSON inválido — 3er fallo (persiste) | Registrar error_json = TRUE + error_operativo. Escalar a HUMANO. Enviar al paciente: 'En este momento un asesor te contactará.' |
| Incoherencia detectada en flujo | Registrar error_operativo. Escalar a HUMANO. |
| Paciente solicita hablar con persona | fase_siguiente = HUMANO. Notificar a asesor ICN. |

| DOCUMENTO 3 — PROMPTS (Versionados) |
| --- |

5. Sistema de Versiones de Prompts

Todos los prompts están versionados. La versión activa se registra en cada interacción.

| Campo en Sheets | Ejemplo | Descripción |
| --- | --- | --- |
| version_prompt | v1.0 | Versión del prompt de fase activo en ese turno |
| version_flujo | v1.0 | Versión de la lógica de flujo de Make activa |

6. Formato JSON Obligatorio de Respuesta (Todas las Fases)

| Formato JSON de respuesta — ChatGPT devuelve SIEMPRE este objeto |
| --- |
| { |
| "respuesta_visible": "Texto que se enviará al paciente por WhatsApp", |
| "notas_internas": "Texto solo visible para equipo clínico ICN", |
| "puntaje_dominio": {"D1": 2, "D2": 0, "D3": 3, "D4": 2, "D5": 2, "D6": 2}, |
| "guia_soporte": "ICHD-3 criterio X / DSM-5-TR criterio Y", |
| "cie10": "G43.009" |
| } |
|  |
| NOTA: nivel_riesgo, score_total, flag_alarma y fase_siguiente son calculados por Make. |
| ChatGPT NO decide la fase siguiente. Solo genera respuesta_visible, notas_internas y puntaje_dominio. |

7. Prompts por Fase — Versión v1.0

7.1 Prompt Base del Sistema (incluir en todas las fases)

| SYSTEM PROMPT BASE — v1.0 |
| --- |
| Eres NeurOrientador, el sistema de teleorientación neurológica de ICN Salud. |
| Tu rol es orientar a los pacientes mediante una evaluación estructurada de riesgo. |
| Eres amable, empático y profesional. |
|  |
| REGLAS ABSOLUTAS (innegociables): |
| 1. Responde SIEMPRE en formato JSON válido (estructura definida). |
| 2. NUNCA emitas diagnóstico definitivo. Lenguaje obligatorio: |
| 'Esto sugiere un nivel de riesgo...' / 'El especialista podrá confirmar...' |
| NUNCA decir: 'Tienes X' / 'Tu diagnóstico es X'. |
| 3. NUNCA formules medicamentos ni recomiendes dosis. |
| 4. SIEMPRE indica en puntaje_dominio el valor numérico de cada dominio respondido. |
| 5. SIEMPRE presenta el servicio como teleorientación, no como consulta médica. |
| 6. Todos los pacientes deben pasar por F3 (teleorientación), sin excepción. |
|  |
| Datos actuales del paciente: |
| - Nombre: {{nombre}} \| Edad: {{edad}} \| Ciudad: {{ciudad}} |
| - Aseguramiento: {{aseguramiento}} \| Fase: {{fase_actual}} |
| - Programa: {{programa_clinico}} \| Riesgo previo: {{nivel_riesgo}} |

7.2 Prompt F0 — Clasificación Inicial (v1.0)

| PROMPT F0 — v1.0 |
| --- |
| {{SYSTEM_PROMPT_BASE}} |
| FASE: F0 — Clasificar intención del primer mensaje. |
|  |
| REGLAS: |
| - Síntomas neurológicos / interés clínico / precio / cita → indica en notas_internas: tipo=teleorientacion |
| - EPS / autorización / historia clínica / admin → indica en notas_internas: tipo=admin |
| (En ADMIN: respuesta_visible incluye link https://icnsalud.com/#contacto) |
| - Prepagada / particular → indica en notas_internas: tipo=teleorientacion |
|  |
| En respuesta_visible: saludo breve ICN Salud. |
| Make determina la fase_siguiente según notas_internas. |

7.3 Prompt F1 — Consentimiento e Identificación (v1.0)

| PROMPT F1 — v1.0 |
| --- |
| {{SYSTEM_PROMPT_BASE}} |
| FASE: F1 — Consentimiento informado + datos básicos. |
|  |
| PASO 1 — Si consentimiento_datos_clinicos = FALSE: |
| Enviar mensaje de consentimiento completo que incluya: |
| (1) Protección de datos (Ley 1581/2012) |
| (2) Naturaleza del servicio: teleorientación, NO consulta médica |
| (3) Uso en investigación ICN (anonimizado) |
| Preguntar por TRES consentimientos por separado: |
| A. ¿Autorizas el tratamiento de tus datos clínicos? (SÍ/NO) |
| B. ¿Aceptas los términos de la teleorientación? (SÍ/NO) |
| C. ¿Autorizas el uso anonimizado de tus datos para investigación? (SÍ/NO) |
| Si A = NO → informar que no puede continuar el flujo → icnsalud.com/#contacto |
| Si B = NO → igual, no puede continuar el flujo |
| Si C = NO → continúa atención, pero no entra en cohorte de investigación |
|  |
| PASO 2 — Capturar: nombre, edad, ciudad, aseguramiento. |
| Si EPS: notas_internas = tipo=admin. Si Prepagada: solicitar nombre de entidad. |
| MÁXIMO 2 preguntas por turno. NO hacer preguntas clínicas aquí. |
|  |
| PASO 3 — Si datos completos: mostrar programas disponibles. Preguntar cuál describe su situación. |
| Make determina fase_siguiente = F2. |

7.4 Prompt F2 — Selección de Problema Neurológico (v1.0)

| PROMPT F2 — v1.0 |
| --- |
| {{SYSTEM_PROMPT_BASE}} |
| FASE: F2 — Seleccionar problema neurológico y confirmar ruta F3. |
|  |
| REGLA: Todos los pacientes pasan por F3. Una teleconsulta = UN problema. |
| Si el paciente pide precio o cita: explicar que primero se hace la evaluación de riesgo. |
|  |
| PASO 1 — Presentar los 10 problemas disponibles: |
| 1. Dolor de cabeza  2. Convulsiones  3. Retraso en neurodesarrollo |
| 4. Temblores y movimientos anormales  5. Problemas de sueño |
| 6. Problemas de memoria  7. ACV  8. Parálisis facial |
| 9. Dolores crónicos  10. Problemas neuromusculares |
|  |
| PASO 2 — Si el paciente menciona múltiples problemas: |
| 'Podemos evaluar un problema por teleconsulta. ¿Cuál le afecta más hoy?' |
| Anotar otros en notas_internas para teleconsultas futuras. |
|  |
| PASO 3 — Señales emocionales fuertes: |
| Si detectas riesgo de autolesión, agotamiento extremo o crisis emocional severa: |
| Indicar en notas_internas: requiere_escalamiento_humano=TRUE. |
| Make escala a HUMANO. No continuar a F3 en esos casos. |
|  |
| Indicar en puntaje_dominio: {problema_seleccionado: numero, programa_clinico: nombre} |

7.5 Prompt F3 — Teleorientación Neurológica (v1.0) — Ejemplo: Cefalea/ICHD-3

| PROMPT F3 — v1.0 (Programa: Cefalea / ICHD-3) |
| --- |
| {{SYSTEM_PROMPT_BASE}} |
| FASE: F3 — Teleorientación neurológica estructurada. |
| Programa: {{programa_clinico}} \| Problema: {{problema_seleccionado}} |
| Guía base: ICHD-3 (Cefalea) \| Adaptar según programa activo. |
|  |
| ÁRBOL CONVERSACIONAL — 6 DOMINIOS (máximo 5–6 turnos totales, 2 preguntas/turno): |
|  |
| D1 BANDERAS ROJAS (prioridad 1 — siempre primero): |
| '¿Ha tenido fiebre, vómito en proyectil, visión doble, pérdida de fuerza, |
| el peor dolor de su vida de inicio súbito, rigidez en la nuca?' |
| Puntaje D1: ninguno = 0 \| uno = 1 \| dos o más = 3 (flag inmediato en notas_internas) |
|  |
| D2 CARACTERIZACIÓN (frecuencia y duración — ICHD-3 Criterio A): |
| '¿Cuántas veces por semana/mes? ¿Desde hace cuánto tiempo?' |
| Puntaje D2: <1/sem = 1 \| 1-2/sem = 2 \| ≥3/sem o crónico = 3 |
|  |
| D3 TIPO Y LOCALIZACIÓN (características del dolor — ICHD-3 Criterio B): |
| '¿El dolor es pulsátil o en presión? ¿En qué zona?' |
| Puntaje D3: pulsátil unilateral = 2 \| bilateral/presión = 1 \| otro = 0 |
|  |
| D4 SEVERIDAD (intensidad e impacto — ICHD-3 Criterio C): |
| '¿Del 0 al 10 cuánto le afecta en su vida diaria?' |
| Puntaje D4: 1-4 = 1 \| 5-7 = 2 \| 8-10 = 3 |
|  |
| D5 FENOTIPO (síntomas asociados — ICHD-3 Criterio C): |
| '¿Sensibilidad a luz, ruido, náuseas, aura visual?' |
| Puntaje D5: uno = 1 \| dos = 2 \| tres o más = 3 |
|  |
| D6 HISTORIAL (tratamiento y respuesta): |
| '¿Ha tomado medicamento? ¿Con qué resultado?' |
| Puntaje D6: sin medicamento/sin efecto = 3 \| efecto parcial = 2 \| buen control = 1 |
|  |
| IMPORTANTE: Solo indica los puntajes en puntaje_dominio. |
| Make calcula el score_total, nivel_riesgo y fase_siguiente. |
|  |
| En respuesta_visible usar SIEMPRE lenguaje de teleorientación: |
| 'Esto sugiere un nivel de riesgo neurológico...' |
| 'El especialista podrá confirmar...' |
| NUNCA decir: 'Tienes X' / 'Tu diagnóstico es X'. |

7.6 Prompt F4 — Conversión Clínica (v1.0)

| PROMPT F4 — v1.0 |
| --- |
| {{SYSTEM_PROMPT_BASE}} |
| FASE: F4 — Conversión clínica y comercial. |
| Riesgo: {{nivel_riesgo}} \| Fenotipo: {{fenotipo_probable}} \| CIE-10: {{cie10}} |
|  |
| ESTRUCTURA OBLIGATORIA de la conversación F4 (no improvisar): |
| T1: Resultado clínico — Resumir hallazgos de la teleorientación con lenguaje prudente. |
| T2: Consecuencia — Explicar brevemente qué implica no actuar a tiempo. |
| T3: Propuesta concreta — Presentar el paquete diagnóstico del programa. |
| T4: Cierre directo — Ofrecer horarios concretos. NO preguntar '¿quieres agendar?' |
| SÍ usar: '¿Te queda mejor el jueves o el viernes?' |
|  |
| MANEJO DE OBJECIONES: |
| 'Es caro' → costo de tratamiento tardío vs. valor del diagnóstico temprano. |
| 'Ya fui al médico' → valor del neurólogo especialista vs. médico general. |
| 'Tengo miedo' → validar, normalizar, enfocar en solución. |
| 'Quiero pensarlo' → respetar, ofrecer info adicional, acordar seguimiento. |
| 'Soy EPS' → redirigir a icnsalud.com/#contacto. |
|  |
| Si paciente pide humano → indicar en notas_internas: requiere_humano=TRUE |
| Si acepta agenda → notas_internas: canal_agenda=Directo |
| Si se redirige a web → notas_internas: canal_agenda=Web |
| Si rechaza completamente → indicar en notas_internas: rechazo=TRUE |
| Make determina fase_siguiente según notas_internas. |

| DOCUMENTO 4 — MODELO DE DATOS |
| --- |

8. Google Sheets — Esquema de Datos MVP

El sistema opera con 4 hojas. Acceso exclusivo a cuentas @icnsalud.com con 2FA.

| 🔐 Control de acceso obligatorio: Solo cuentas @icnsalud.com con 2FA. Make accede mediante cuenta de servicio con permisos mínimos. Auditoría mensual. Sin links compartidos abiertos. |
| --- |

8.1 Hoja 1: PACIENTES — Campos MVP

| Campo | Tipo | Descripción |
| --- | --- | --- |
| paciente_id | Texto (auto) | ID único. Clave: PAC-YYYYMMDD-NNN |
| telefono | Texto | Número WhatsApp — CLAVE PRIMARIA. Validar antes de crear nuevo registro. |
| nombre | Texto | Capturado en F1 |
| edad | Número | Edad en años |
| ciudad | Texto | Ciudad de residencia |
| aseguramiento | Texto | Particular / Prepagada |
| entidad_prepagada | Texto | Nombre de la prepagada si aplica |
| consentimiento_datos_clinicos | Booleano | TRUE si autorizó tratamiento de datos clínicos (OBLIGATORIO para continuar flujo) |
| consentimiento_teleorientacion | Booleano | TRUE si aceptó términos de teleorientación (OBLIGATORIO para continuar flujo) |
| consentimiento_investigacion | Booleano | TRUE si autorizó uso anonimizado en investigación ICN (OPCIONAL — sin esto, atención continúa pero NO se inserta en COHORTES) |
| timestamp_consentimiento | Fecha-hora | Momento de aceptación |
| fase_actual | Texto | F0 / F1 / F2 / F3 / F4 / ADMIN / HUMANO |
| tipo_consulta | Texto | teleorientacion / agendar / reformulacion / resultados |
| programa_clinico | Texto | Cefalea / Epilepsia / Sueño / Memoria / ACV / etc. |
| problema_seleccionado | Número (1-10) | Problema neurológico elegido en F2 |
| guia_soporte | Texto | Guía clínica que soporta la clasificación (ej: ICHD-3 G43.009) |
| cie10 | Texto | Código CIE-10 del fenotipo probable |
| nivel_riesgo | Texto | Bajo / Moderado / Alto / Alarma — Calculado por Make |
| score_total | Número | Puntaje acumulado D1–D6 — Calculado por Make |
| fenotipo_probable | Texto | Fenotipo clínico probable (sin diagnóstico definitivo) |
| respuestas_orientacion | JSON (Texto) | Respuestas del paciente a los 6 dominios D1–D6 |
| reporte_enviado | Booleano | TRUE si ya se envió el mensaje de reporte de riesgo |
| conversion | Texto | Tipo de conversión lograda en F4 |
| fecha_cita | Fecha | Fecha de cita agendada |
| canal_agenda | Texto | Directo (agente) / Web (redirección) |
| estado_cita | Texto | Pendiente / Confirmada / Asistió / No asistió |
| fecha_primera_orientacion | Fecha | Primera teleorientación completada |
| fecha_ultima_orientacion | Fecha | Última teleorientación (control cada 6 meses) |
| cohorte | Texto | programa + riesgo + fenotipo. Solo si consentimiento_investigacion = TRUE |
| requiere_humano | Booleano | TRUE si se activó escalamiento a asesor |
| requiere_revision_medica | Booleano | TRUE si el caso requiere revisión del equipo médico ICN |
| motivo_escalamiento | Texto | Descripción del motivo del escalamiento a HUMANO |
| error_json | Booleano | TRUE si ocurrió error de JSON persistente en ChatGPT |
| error_operativo | Texto | Descripción del error técnico si aplica |
| version_prompt | Texto | Versión del prompt activo (ej: v1.0) |
| version_flujo | Texto | Versión del flujo Make activo (ej: v1.0) |
| historial_json | JSON (Texto) | Array de mensajes para contexto (máximo 15–20 turnos) |
| notas_internas | Texto | Campo libre para equipo clínico ICN |
| fecha_creacion | Fecha-hora | Timestamp de primer contacto |
| ultima_actividad | Fecha-hora | Timestamp del último mensaje |

8.2 Hoja 2: CONVERSACIONES

Una fila por turno. Auditoría completa de cada interacción.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| conv_id | Texto (auto) | ID único: CONV-{paciente_id}-{timestamp} |
| paciente_id | Texto | FK → PACIENTES |
| telefono | Texto | Número WhatsApp (lookup rápido) |
| fase | Texto | Fase activa en ese turno |
| mensaje_usuario | Texto | Mensaje exacto del paciente |
| respuesta_agente | Texto | Respuesta generada por ChatGPT y enviada |
| guia_soporte_turno | Texto | Guía clínica que soportó la decisión en ese turno |
| timestamp | Fecha-hora | Fecha y hora del turno |
| tokens_usados | Número | Tokens consumidos en la llamada |
| flag_alarma | Booleano | TRUE si el turno activó una bandera roja |
| escalado_humano | Booleano | TRUE si en ese turno se notificó al neuroasesor |
| version_prompt | Texto | Versión del prompt activo en ese turno |

8.3 Hoja 3: CITAS

Una fila por cita. Para MVP: agenda manual con confirmación del agente.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| cita_id | Texto (auto) | ID único: CITA-{paciente_id}-{fecha} |
| paciente_id | Texto | FK → PACIENTES |
| tipo | Texto | Consulta / Paquete diagnóstico / Tratamiento |
| programa | Texto | Programa clínico asociado |
| fecha_cita | Fecha | Fecha programada |
| hora_cita | Texto | Hora programada |
| canal_agenda | Texto | Directo (agente) / Web |
| confirmacion | Texto | Pendiente / Confirmada / Cancelada |
| seguimiento_post | Booleano | TRUE si ya se realizó seguimiento postconsulta (manual en MVP) |
| resultado_post | Texto | Medicamentos / Terapias / Exámenes / Sin novedad |

8.4 Hoja 4: COHORTES_INVESTIGACION

| ⚠️ REGLA CRÍTICA: Inserción condicional OBLIGATORIA: Antes de guardar cualquier dato en esta hoja, Make valida consentimiento_investigacion = TRUE. Si es FALSE, no se inserta ningún dato. Solo lectura para el equipo de investigación. |
| --- |

| Campo | Descripción |
| --- | --- |
| cohorte_id | ID único de la entrada en investigación |
| programa_clinico | Programa neurológico evaluado |
| guia_soporte | Guía clínica base de la clasificación |
| cie10 | Código CIE-10 del fenotipo probable |
| nivel_riesgo | Bajo / Moderado / Alto / Alarma |
| fenotipo_probable | Fenotipo clínico identificado (sin datos personales) |
| score_total | Puntaje numérico total |
| respuestas_orientacion | JSON con respuestas D1–D6 (sin datos personales) |
| edad | Edad del paciente (anonimizado) |
| ciudad | Ciudad (anonimizado, solo para epidemiología) |
| fecha_evaluacion | Fecha de la teleorientación (anonimizado) |
| conversion | ¿Se convirtió a consulta/paquete? Sí/No |

8.5 Reglas de Validación de Datos

| Regla de validación | Implementación en Make |
| --- | --- |
| Control de duplicados por teléfono | Antes de crear nuevo paciente: buscar en PACIENTES por teléfono. Si existe → actualizar fila existente. Si no → crear nueva fila. |
| Consentimiento clínico obligatorio | Si consentimiento_datos_clinicos = FALSE o consentimiento_teleorientacion = FALSE → no continuar flujo. Enviar link icnsalud.com/#contacto. |
| Inserción en cohortes condicionada | Si consentimiento_investigacion = FALSE → no insertar en COHORTES_INVESTIGACION. Solo registrar en PACIENTES y CONVERSACIONES. |
| Historial limitado a 15–20 turnos | Antes de agregar turno: contar array. Si >15 → eliminar el turno más antiguo. Stringificar y guardar. |
| Formato del campo cohorte | Solo generar si consentimiento_investigacion = TRUE. Formato: {programa}_{riesgo}_{fenotipo_abreviado} |

9. Tabla de Fases — MVP

| Fase | Nombre | Objetivo | Condición de transición | Naturaleza |
| --- | --- | --- | --- | --- |
| F0 | Clasificación | Detectar tipo de consulta | Teleorientación → F1 \| Admin → ADMIN | Teleorientación |
| F1 | Identificación | Consentimiento + datos básicos | Datos OK → F2 | Teleorientación |
| F2 | Selección | Confirmar ruta F3 + elegir 1 problema | Señal fuerte → HUMANO \| Normal → F3 | Teleorientación |
| F3 | Orientación | Árbol clínico + scoring + reporte | Bajo → (registrar, no F6 en MVP) \| Mod/Alto → F4 \| Alarma → HUMANO | Teleorientación |
| F4 | Conversión | Agenda + paquete diagnóstico | Acepta → CITAS \| Rechaza → fin \| Humano → HUMANO | Comercial |
| ADMIN | Administrativo | Redirigir a canal ICN | Fin en agente → link web | Administrativo |
| HUMANO | Escalamiento | Transferir a neuroasesor | Notificación ICN → fin agente | Escalado |

| 📌 Nota: F5 y F6 quedan pospuestos para V2. En MVP, los pacientes de bajo riesgo son registrados pero no reciben seguimiento automático. |
| --- |

10. Escalamiento Obligatorio a Humano

| Trigger | Descripción | Acción |
| --- | --- | --- |
| Filtro de alarma (pre-ChatGPT) | Palabras clave detectadas en mensaje bruto del paciente | NO llamar a ChatGPT. Activar flag_alarma. Notificar neuroasesor. Orientar a urgencias si aplica. |
| flag_alarma en D1 (F3) | Score D1 = 2 o más banderas rojas detectadas en árbol clínico | fase_siguiente = HUMANO. Notificar neuroasesor con resumen clínico. |
| Error JSON persistente | JSON inválido después de 2 reintentos | Registrar error_json = TRUE. Escalar a HUMANO. Mensaje de espera al paciente. |
| Señal emocional fuerte (F2) | Riesgo de autolesión o crisis severa detectada | fase_siguiente = HUMANO inmediatamente. |
| Solicitud del paciente | Paciente pide hablar con una persona | fase_siguiente = HUMANO. Notificar asesor ICN. |
| EPS detectada | Paciente es usuario de EPS | fase_siguiente = ADMIN. Redirigir a icnsalud.com/#contacto. |
| Duda clínica del sistema | IA no puede clasificar con certeza | Registrar motivo_escalamiento. fase_siguiente = HUMANO. |

11. Resumen Ejecutivo V4 — Decisiones Clave

| ✅ LO QUE SE HACE EN V4 (MVP) |
| --- |
| Implementar solo F0, F1, F2, F3 y F4 Mover lógica crítica (score, riesgo, alarma, fases) de ChatGPT a Make (backend) Implementar filtro de palabras clave de alarma ANTES de llamar a ChatGPT Validar JSON con reintento automático (máx 2) y fallback a HUMANO Separar los 3 consentimientos en campos independientes Condicionarán inserción en COHORTES a consentimiento_investigacion = TRUE Simplificar F2.5 a detección básica de señales fuertes (escalar o continuar) Usar mensaje de texto estructurado como reporte de riesgo (sin imagen en MVP) Agregar campos de control: error_json, error_operativo, version_prompt, motivo_escalamiento Versionar todos los prompts desde v1.0 Usar lenguaje correcto: 'base inicial para análisis clínico' (no 'validado') |

| 🚫 LO QUE NO SE HACE EN MVP |
| --- |
| Lanzar con toda la complejidad de V3 Depender totalmente de prompts de IA para lógica clínica crítica Implementar F5 (seguimiento automático) o F6 (educación recurrente) Implementar ESRI (contexto geográfico) Activar automatización completa de investigación desde el inicio Mezclar operación clínica e investigación sin control de consentimiento Implementar modelos predictivos o análisis avanzado de cohortes Generar imagen del reporte (pospuesto para V2) |

12. Base Clínica y Metodológica (Referencia)

Todo el flujo clínico de NeurOrientador está fundamentado en guías de manejo validadas internacionalmente y adoptadas por ICN Salud. El lenguaje correcto para este sistema en etapa inicial es:

'datos estructurados para futura validación' y 'base inicial para análisis clínico'.

| Programa | Guía base | Versión | CIE-10 de salida | Estado MVP |
| --- | --- | --- | --- | --- |
| Cefalea / Migraña | ICHD-3 | 3ra edición, 2018 | G43.x / G44.x | ✅ Activo |
| Neurodesarrollo | DSM-5-TR (APA) | 2022 | F84.x / F90.x | ✅ Activo |
| Epilepsia | Guía ILAE 2017 | 2017/actualizada | G40.x | ✅ Activo |
| Trastornos del sueño | ICSD-3 (AASM) | 3ra edición | G47.x | ✅ Activo |
| Memoria / Cognitivo | Guías NIA-AA + ICN | 2018/ICN | F06.7 / G30.x | ✅ Activo |
| ACV | Guía AHA/ASA + ICN | 2021/ICN | I63.x / I60.x | ✅ Activo |
| Parálisis facial | Guía práctica EAN | 2019 | G51.0 | ✅ Activo |
| Movimiento / Parkinson | Guías MDS | 2020 | G20 / G25.x | ✅ Activo |
| Dolor neuropático | Guías IASP + NeuPSIG | 2019 | G62.x | ✅ Activo |
| Neuromuscular | Guías AANEM + ICN | ICN | G70.x / G71.x | ✅ Activo |

| DOCUMENTO 5 — NEUROASISTENTE Trazabilidad, Registro y Retroalimentación Continua |
| --- |

13. Rol del NeuroAsistente — Principio de Auditoría Total

| 🎯 PRINCIPIO FUNDAMENTAL: El NeuroAsistente no opera como una capa invisible.Todo contacto con el paciente debe quedar registrado, trazado y disponible para revisión.Objetivo: no solo operar, sino aprender y mejorar continuamente. |
| --- |

El NeuroAsistente es el componente del sistema responsable del acompañamiento al paciente después de completar la teleorientación (F3/F4). A diferencia del flujo conversacional principal (NeurOrientador), el NeuroAsistente puede actuar de forma proactiva — contactando al paciente para confirmar citas, resolver dudas, hacer seguimiento postconsulta y detectar oportunidades de mejora o de atención adicional.

Para que este componente sea auditable, trazable y útil para la mejora continua del sistema, cada interacción debe quedar registrada de forma estructurada en la base de datos.

13.1 Tipos de Interacción del NeuroAsistente

| Tipo de interacción | Descripción | Escalamiento posible |
| --- | --- | --- |
| confirmacion_cita | El NeuroAsistente contacta al paciente para confirmar asistencia a cita agendada. | Comercial si cancela |
| preparacion_cita | Envía instrucciones de preparación (ayuno, documentos, qué llevar, modalidad). | Clínico si hay duda médica |
| recordatorio | Recordatorio 3 días o 1 día antes de la cita con datos clave. | Comercial si no responde |
| seguimiento_post_cita | Contacto después de la consulta para conocer el resultado y próximo paso. | Clínico o comercial según respuesta |
| resolucion_duda | Respuesta a pregunta del paciente sobre el proceso, la cita o el resultado. | Clínico si es duda médica |
| acompañamiento | Mensaje de apoyo en caso de señal emocional o contexto de vulnerabilidad. | Clínico si hay riesgo |
| oportunidad_comercial | Detección de interés en nuevo programa o consulta adicional. | Comercial |

13.2 Hoja 5: NEUROASISTENTE_INTERACCIONES — Esquema de Datos

| 📋 NUEVA HOJA: Esta hoja es nueva en V4.1. No existía en versiones anteriores.Se crea automáticamente en Google Sheets dentro del mismo archivo del sistema.Una fila por cada contacto del NeuroAsistente con el paciente.Acceso restringido igual que las demás hojas: solo cuentas @icnsalud.com con 2FA. |
| --- |

| Campo | Tipo | Descripción y reglas de validación |
| --- | --- | --- |
| interaccion_id | Texto (auto) | ID único generado por Make. Formato: NA-{paciente_id}-{timestamp}. Ejemplo: NA-PAC-20260320-001-20260326T090000 |
| paciente_id | Texto | FK → PACIENTES. Obligatorio. Validar que el paciente existe antes de insertar. |
| cita_id | Texto | FK → CITAS. Obligatorio si la interacción está relacionada con una cita. Puede quedar vacío en interacciones de acompañamiento general. |
| fecha_hora | Fecha-hora | Timestamp exacto del momento en que el NeuroAsistente envía el mensaje. Formato ISO 8601. Generado automáticamente por Make. |
| canal_contacto | Texto | Canal utilizado. Valores válidos: WhatsApp \| Email \| SMS. En MVP siempre WhatsApp. |
| tipo_interaccion | Texto | Tipo de contacto. Valores válidos: confirmacion_cita \| preparacion_cita \| recordatorio \| seguimiento_post_cita \| resolucion_duda \| acompañamiento \| oportunidad_comercial |
| mensaje_enviado | Texto | Texto completo del mensaje enviado al paciente por el NeuroAsistente. Obligatorio. |
| respuesta_paciente | Texto | Respuesta exacta del paciente. Si no responde en 24h: registrar 'sin_respuesta'. Si responde después: actualizar el campo. |
| estado_interaccion | Texto | Estado actual de la interacción. Valores: enviado \| respondido \| pendiente \| cerrado \| escalado |
| requiere_revision_clinica | Booleano | TRUE si la respuesta del paciente contiene señal clínica (complicación, duda médica, síntoma nuevo, riesgo). Activa revisión por equipo médico ICN. |
| requiere_revision_comercial | Booleano | TRUE si la respuesta del paciente contiene señal comercial (cancelación, interés en nuevo programa, objeción de precio, recomendación a tercero). Activa seguimiento comercial. |
| notas_internas | Texto | Observaciones del NeuroAsistente o del equipo ICN sobre la interacción. Visible solo para el equipo. No se comparte con el paciente. |
| responsable | Texto | Quién generó la interacción. Valores: NeuroAsistente_automatico \| Neuroasesor_humano \| Sistema_Make. Permite distinguir interacciones automáticas de manuales. |
| accion_generada | Texto | Acción concreta que se disparó a partir de esta interacción. Ejemplos: ninguna \| cita_confirmada \| cita_reprogramada \| escalado_clinico \| escalado_comercial \| nueva_teleconsulta_agendada |
| version_flujo | Texto | Versión del flujo del NeuroAsistente activo en el momento de la interacción. Ejemplo: v1.0. Permite rastrear cambios de comportamiento entre versiones. |
| timestamp_actualizacion | Fecha-hora | Última actualización del registro (ej: cuando el paciente responde después de haber marcado estado=enviado). |

13.3 Flujo de Registro en Make — Escenario NeuroAsistente

Cada vez que el NeuroAsistente actúa, Make ejecuta el siguiente flujo de registro:

| Paso | Acción en Make |
| --- | --- |
| 1 | TRIGGER — El NeuroAsistente se activa (por schedule, por evento de cita, o por mensaje entrante del paciente relacionado con una cita existente). |
| 2 | GOOGLE SHEETS — Recuperar datos del paciente (paciente_id, nombre, cita_id, programa_clinico, fase_actual, historial reciente). |
| 3 | ChatGPT API (opcional) — Si la interacción requiere lenguaje personalizado (ej: seguimiento post cita), generar el mensaje con el contexto del paciente. Si es recordatorio estático, usar plantilla fija. |
| 4 | WHATSAPP — Enviar mensaje al paciente. Registrar timestamp exacto. |
| 5 | GOOGLE SHEETS — Insertar fila en NEUROASISTENTE_INTERACCIONES con: interaccion_id (auto), paciente_id, cita_id, fecha_hora, canal_contacto, tipo_interaccion, mensaje_enviado, estado_interaccion = 'enviado', responsable, version_flujo. |
| 6 | ESPERAR RESPUESTA — Cuando el paciente responde: Make detecta el mensaje entrante y lo asocia al interaccion_id correspondiente (por paciente_id + cita_id + estado=enviado más reciente). |
| 7 | ANÁLISIS DE RESPUESTA — Make + ChatGPT evalúan el contenido de la respuesta del paciente y determinan: requiere_revision_clinica (TRUE/FALSE) y requiere_revision_comercial (TRUE/FALSE). |
| 8 | GOOGLE SHEETS — Actualizar la fila en NEUROASISTENTE_INTERACCIONES: respuesta_paciente, estado_interaccion = 'respondido', requiere_revision_clinica, requiere_revision_comercial, accion_generada, timestamp_actualizacion. |
| 9 | ROUTER — Si requiere_revision_clinica = TRUE: notificar al equipo médico ICN con resumen de la interacción. Si requiere_revision_comercial = TRUE: notificar al asesor comercial. |
| 10 | Si no hay respuesta en 24h: Make ejecuta paso de seguimiento → actualizar estado_interaccion = 'pendiente'. Si no responde en 48h adicionales: estado = 'cerrado' + notas_internas = 'sin respuesta tras 2 intentos'. |

13.4 Lógica de Escalamiento desde NeuroAsistente

| Señal detectada en respuesta del paciente | requiere_revision_clinica | requiere_revision_comercial | Acción generada |
| --- | --- | --- | --- |
| Complicación clínica post consulta (dolor, reacción, síntoma nuevo) | TRUE | FALSE | Notificar equipo médico ICN + registrar accion_generada = escalado_clinico |
| No entendió indicaciones médicas del especialista | TRUE | FALSE | Notificar equipo médico + notas_internas con detalle de la duda |
| Duda sobre medicamento recetado | TRUE | FALSE | Escalar a neuroasesor clínico. No responder directamente. |
| Señal emocional o angustia expresada | TRUE | FALSE | Escalar a HUMANO (neuroasesor). Registrar en notas_internas. |
| Inconformidad con el servicio | FALSE | TRUE | Notificar asesor comercial + registrar accion_generada = escalado_comercial |
| Interés en nuevo programa o consulta adicional | FALSE | TRUE | Registrar oportunidad. Notificar asesor comercial. accion_generada = nueva_teleconsulta_agendada (si se concreta) |
| Cancelación de cita sin reagendar | FALSE | TRUE | Notificar asesor comercial para seguimiento. accion_generada = cita_reprogramada o cerrado |
| Respuesta normal / confirmación | FALSE |  | accion_generada = ninguna. Estado = cerrado. |

13.5 Objetivo del Registro — Más Allá de la Operación

El registro de interacciones del NeuroAsistente cumple cuatro funciones estratégicas:

| Función | Qué permite hacer |
| --- | --- |
| Auditoría operativa | Saber exactamente qué se dijo, cuándo, quién lo envió, qué respondió el paciente y qué acción se generó. Revisable en cualquier momento por el equipo ICN. |
| Control de calidad | Detectar inconsistencias en mensajes, errores de información, respuestas inadecuadas del sistema o del asesor humano. Base para auditorías periódicas. |
| Detección de patrones | Identificar qué dudas aparecen con más frecuencia, qué tipo de pacientes requieren más acompañamiento, qué mensajes generan mayor tasa de respuesta. |
| Retroalimentación del sistema | Usar los datos de NEUROASISTENTE_INTERACCIONES para ajustar prompts, mejorar mensajes de recordatorio, optimizar tiempos de contacto y refinar los criterios de escalamiento. |

13.6 Modelo de Retroalimentación Futura (V2)

El esquema de datos está diseñado para soportar análisis de aprendizaje en versiones posteriores. Los campos clave para ese análisis son:

| Campo analítico | Pregunta que responde | Aplicación en V2 |
| --- | --- | --- |
| tipo_interaccion + estado_interaccion | ¿Qué tipos de contacto generan más respuesta del paciente? | Optimizar cuándo y cómo contactar para mejorar adherencia |
| respuesta_paciente (texto libre) | ¿Qué dudas y preocupaciones expresan los pacientes? | Entrenar modelo de categorización automática de respuestas |
| requiere_revision_clinica / comercial | ¿Qué porcentaje de interacciones escala? | Ajustar umbrales de escalamiento y reducir carga del equipo humano |
| accion_generada + conversion (PACIENTES) | ¿Qué mensajes del NeuroAsistente generan mayor conversión? | A/B testing de mensajes. Identificar los más efectivos. |
| fecha_hora + estado = sin_respuesta | ¿En qué horarios hay menor tasa de respuesta? | Ajustar ventanas de contacto por franja horaria |
| version_flujo + tasa de escalamiento | ¿Las nuevas versiones del NeuroAsistente reducen errores? | Comparar versiones y validar mejoras antes de producción |
| tipo_interaccion = seguimiento_post_cita + resultado_post (CITAS) | ¿El acompañamiento post cita mejora la adherencia al tratamiento? | Medir impacto del NeuroAsistente en continuidad de atención |

13.7 Relación del NeuroAsistente con las Demás Hojas del Sistema

| Diagrama de relaciones — NEUROASISTENTE_INTERACCIONES |
| --- |
| PACIENTES (1) ─────────────────── (N) NEUROASISTENTE_INTERACCIONES |
| │                                         │ |
| │  paciente_id (FK)                       │  cita_id (FK) |
| │                                         │ |
| CITAS (1) ──────────────────────── (N) NEUROASISTENTE_INTERACCIONES |
|  |
| Campos de lectura cruzada recomendados en dashboard: |
| PACIENTES.nivel_riesgo → contexto clínico del paciente |
| PACIENTES.programa_clinico → personalizar mensaje según programa |
| CITAS.fecha_cita + CITAS.confirmacion → determinar tipo de interacción |
| CITAS.resultado_post → base para seguimiento post consulta |
| CONVERSACIONES → historial previo para evitar mensajes repetitivos |

| ⚙️ Nota técnica Make: IMPORTANTE para el equipo técnico:El campo interaccion_id debe generarse como: NA-{paciente_id}-{YYYYMMDDTHHmmss}Esto garantiza que sea único globalmente y ordenable cronológicamente.Make debe buscar siempre por paciente_id + estado='enviado' + cita_id para asociar respuestas entrantes al registro correcto.Si un paciente envía un mensaje no relacionado con ninguna cita activa → derivar a Escenario 1 (flujo NeurOrientador). |
| --- |

13.8 Checklist de Implementación — NeuroAsistente MVP

|  | Tarea de implementación | Estado |
| --- | --- | --- |
| □ | Crear hoja NEUROASISTENTE_INTERACCIONES en Google Sheets con todos los campos definidos | Pendiente |
| □ | Configurar permisos de acceso: solo cuentas @icnsalud.com + cuenta de servicio Make | Pendiente |
| □ | Crear Escenario Make para trigger de confirmación de cita (1 día antes) | Pendiente |
| □ | Crear Escenario Make para trigger de preparación de cita (3 días antes) | Pendiente |
| □ | Crear Escenario Make para seguimiento post consulta (1 día después) | Pendiente |
| □ | Implementar lógica de asociación de respuesta entrante a interaccion_id | Pendiente |
| □ | Implementar análisis de respuesta (ChatGPT) para determinar requiere_revision_clinica / comercial | Pendiente |
| □ | Configurar notificación a equipo médico ICN cuando requiere_revision_clinica = TRUE | Pendiente |
| □ | Configurar notificación a asesor comercial cuando requiere_revision_comercial = TRUE | Pendiente |
| □ | Implementar manejo de 'sin respuesta' después de 24h y 48h | Pendiente |
| □ | Registrar version_flujo en cada interacción desde el inicio (v1.0) | Pendiente |
| □ | Validar con equipo ICN los mensajes plantilla para cada tipo_interaccion | Pendiente |

| NeurOrientador V4.1 — ICN Salud Datos estructurados para futura validación  ·  Base inicial para análisis clínico Stack: WhatsApp Business API  ·  Make  ·  ChatGPT API (GPT-4o)  ·  Google Sheets  ·  2026 |
| --- |



---

# FUENTE V3: NeuroOrientador V3 (1).docx

**Rol de esta fuente:** Versión clínica ampliada con F2.5 y detalles psicosociales; usar solo si V6/V5 no contradicen.


NeurOrientador

ICN Salud — Sistema Clínico de Teleorientación Neurológica

Documentación Técnica de Implementación — Versión 3.0

Stack: WhatsApp Business API  ·  Make  ·  ChatGPT API  ·  Google Sheets

Base metodológica: ICHD-3 · DSM-5-TR · Guías ICN · Modelo UNI de Evaluación de Riesgo en Salud

2026

| Canal WhatsApp Business API | Automatización Make | IA ChatGPT API (GPT-4o) | Datos Google Sheets |
| --- | --- | --- | --- |

1. Base Clínica y Metodológica

Todo el flujo clínico de NeurOrientador está fundamentado en guías de manejo validadas internacionalmente y adoptadas por ICN Salud. Cada decisión del árbol conversacional tiene trazabilidad directa a un criterio clínico documentado.

1.1 Marco metodológico principal — Modelo UNI de Evaluación de Riesgo en Salud

| Modelo UNI — Fundamento del sistema de puntuación y clasificación |
| --- |
| Todo el flujo de NeurOrientador parte del Modelo de Evaluación de Riesgo en Salud UNI, |
| desarrollado por ICN Salud. Este modelo define: |
|  |
| • La lógica de puntuación por dominios (D1–D6) |
| • Los umbrales de clasificación: Bajo / Moderado / Alto / Alarma |
| • Las rutas de salida según el nivel de riesgo calculado |
| • Los fenotipos clínicos probables por programa |
|  |
| El sistema de scoring de F3 implementa directamente este modelo, |
| asignando pesos a cada respuesta según los criterios UNI validados por el equipo médico ICN. |

1.2 Guías clínicas por programa y correspondencia CIE-10

| Programa | Guía base | Versión | Criterios aplicados en F3 | Clasificación CIE-10 de salida |
| --- | --- | --- | --- | --- |
| Cefalea / Migraña | ICHD-3 (International Headache Classification) | 3ra edición, 2018 | Criterios A–E para migraña con/sin aura, tipo, frecuencia, severidad, respuesta a analgésicos | G43.x (Migraña), G44.x (Otras cefaleas) |
| Neurodesarrollo | DSM-5-TR (APA) | 2022 | Criterios de TDAH (Criterio A–E), TEA (Criterios A–B), retraso del desarrollo | F84.x (TEA), F90.x (TDAH), F88 (Retraso) |
| Epilepsia | Guía ILAE 2017 + Guía MPS Colombia | 2017 / actualizada | Tipo de crisis, frecuencia, adherencia, triggers, impacto funcional | G40.x (Epilepsia) |
| Trastornos del sueño | ICSD-3 (American Academy of Sleep Medicine) | 3ra edición | Insomnio, higiene del sueño, somnolencia, apnea sospechada | G47.x (Trastornos del sueño) |
| Memoria / Deterioro cognitivo | Guías NIA-AA + Guías ICN | 2018 / ICN | MMSE adaptado conversacional, inicio, progresión, impacto en ABVD | F06.7 (DCL), G30.x (Alzheimer), F03 (Demencia NE) |
| ACV | Guía AHA/ASA + Guías ICN | 2021 / ICN | FAST adaptado, factores de riesgo, tiempo de inicio — protocolo alarma estricta | I63.x (Infarto cerebral), I60.x (Hemorragia) |
| Parálisis facial | Guía práctica EAN | 2019 | Grado House-Brackmann adaptado, tiempo de inicio, compromiso ocular | G51.0 (Parálisis de Bell) |
| Movimiento / Parkinson | Guías MDS | 2020 | Escala MDS-UPDRS adaptada conversacional, tipo de temblor, rigidez, bradicinesia | G20 (Parkinson), G25.x (Otros mov.) |
| Dolor neuropático | Guías IASP + NeuPSIG | 2019 | DN4 adaptado conversacional, distribución, características, comorbilidades | G62.x (Neuropatía) |
| Neuromuscular | Guías AANEM + ICN | ICN | Debilidad, distribución, progresión, compromiso respiratorio | G70.x (Unión NM), G71.x (Miopatía) |

1.3 Trazabilidad clínica — Campo obligatorio en cada decisión

Cada decisión de clasificación del sistema debe registrar qué guía soporta la decisión. Este campo es obligatorio en el dashboard interno de F3 y en la hoja Google Sheets.

| Ejemplo de campo guia_soporte en respuesta JSON de ChatGPT (F3) |
| --- |
| { |
| "respuesta_visible": "Con base en lo que me contaste...", |
| "fase_siguiente": "F4", |
| "campos_actualizar": { |
| "nivel_riesgo": "Alto", |
| "fenotipo_probable": "Migraña episódica de alta frecuencia" |
| }, |
| "guia_soporte": "ICHD-3 — Criterios A-E migraña sin aura (G43.009)", |
| "cie10": "G43.009", |
| "flag_alarma": false, |
| "notas_internas": "Score 13/15. Criterio ICHD-3 cumplido: ≥5 episodios, 4-72h, pulsátil unilateral, intensidad moderada-severa, náuseas, fotofobia." |
| } |

2. Arquitectura Técnica del Sistema

NeurOrientador integra tres capas tecnológicas orquestadas por Make. El canal de entrada es WhatsApp Business API, la inteligencia está en ChatGPT (GPT-4o) y la persistencia de datos opera en Google Sheets.

2.1 Diagrama de flujo de datos

| Flujo de datos — Arquitectura completa |
| --- |
| USUARIO (WhatsApp) |
| ↓  mensaje entrante |
| WHATSAPP BUSINESS API → webhook HTTP POST → Make |
| ↓ |
| MAKE — Escenario 1 (conversación principal) |
| ├─ Buscar paciente en Google Sheets (por teléfono) |
| ├─ Recuperar historial_json + fase_actual + datos clínicos |
| ├─ Seleccionar system prompt según fase_actual |
| ├─ Llamar ChatGPT API (GPT-4o) con contexto completo |
| ├─ Parsear respuesta JSON estructurada |
| ├─ Actualizar Google Sheets (paciente + conversaciones + citas) |
| ├─ Si flag_alarma = TRUE → notificar humano |
| └─ Enviar respuesta_visible al paciente por WhatsApp |
| ↓  (si aplica) |
| MAKE — Escenario 2: generar imagen reporte visual → enviar por WhatsApp |
| ↓  (programado) |
| MAKE — Escenario 3: recordatorios F5 (diario 8am) |
| MAKE — Escenario 4: seguimiento preventivo F6 (lunes, miércoles, viernes 9am) |

2.2 Stack tecnológico

| Componente | Herramienta | Rol | Consideraciones clave |
| --- | --- | --- | --- |
| Canal | WhatsApp Business API (Meta Cloud API) | Recibir y enviar mensajes | Número verificado en Meta Business Manager. Webhook activo 24/7 |
| Orquestador | Make — plan Core o superior | Conectar todos los módulos, gestionar flujo, enrutar fases | Escenario principal activo permanentemente. Alertas de error configuradas |
| Inteligencia artificial | ChatGPT API — GPT-4o | Procesar mensajes, aplicar lógica de fase, generar respuestas JSON | Historial completo enviado en cada llamada. Respuesta siempre en JSON estructurado |
| Base de datos | Google Sheets | Pacientes, conversaciones, citas, cohortes de investigación | Control de acceso estricto. Solo cuentas ICN autorizadas. 4 hojas operativas |
| Generación de reporte visual | Make + servicio de imagen (API imgbb o similar) | Generar imagen del reporte de riesgo al cierre de F3/F4 | Imagen enviada por WhatsApp. Incluye disclaimer legal obligatorio |
| Agenda particulares | Google Calendar o Calendly API (vía Make) | Consultar disponibilidad y agendar en F4 | Bloques específicos para particulares definidos con Jeneth. Redirección a web como alternativa |
| Notificación humano | WhatsApp número interno ICN / Email | Alertar a neuroasesor en casos de alarma o solicitud | Mensaje estructurado con: nombre, teléfono, síntoma, resumen clínico |

3. Consentimiento Informado — F1 (Obligatorio legal)

El consentimiento informado es el primer paso obligatorio de F1 antes de capturar cualquier dato del paciente. Debe cubrir cuatro elementos legales, quedar registrado en Google Sheets y usar lenguaje claro y accesible.

3.1 Componentes obligatorios del consentimiento

| Componente | Contenido obligatorio | Base legal | Registro en Sheets |
| --- | --- | --- | --- |
| Tratamiento de datos | Informar que los datos personales y de salud serán tratados con confidencialidad. Indicar finalidad: orientación clínica, investigación anonimizada ICN, seguimiento. | Ley 1581 de 2012 — Habeas Data. Decreto 1377 de 2013. | Campo: consentimiento_datos = TRUE/FALSE + timestamp |
| Naturaleza del servicio | Explicar que esto es una teleorientación en salud neurológica, no una consulta médica. El resultado es una clasificación de riesgo, no un diagnóstico. | Res. 2654/2019 — Teleorientación en salud | Campo: consentimiento_servicio = TRUE/FALSE |
| Alcance del sistema | Informar que el agente NO diagnostica, NO formula medicamentos y NO reemplaza al especialista. | Ley 23 de 1981 — Ética médica | Incluido en consentimiento_servicio |
| Uso en investigación | Informar que los datos anonimizados podrán ser usados para investigación clínica ICN e identificación de patrones poblacionales. | Res. 8430 de 1993 — Investigación en salud | Campo: consentimiento_investigacion = TRUE/FALSE |

3.2 Texto exacto del consentimiento (mensaje F1)

| MENSAJE DE CONSENTIMIENTO — Enviar al inicio de F1 Hola, bienvenido/a a ICN Salud. Soy NeurOrientador, el sistema de teleorientación neurológica de ICN Salud. Antes de comenzar, necesito informarte tres cosas importantes: 1. PROTECCIÓN DE DATOS: Tu información personal y de salud será tratada con confidencialidad según la Ley 1581 de 2012. Tus datos se usarán solo para orientarte y, de forma anonimizada, para mejorar nuestros protocolos clínicos. 2. NATURALEZA DEL SERVICIO: Este es un servicio de TELEORIENTACIÓN en salud neurológica. El resultado que obtendrás es una evaluación de riesgo, NO un diagnóstico médico. No reemplaza la consulta con un especialista neurólogo. 3. LO QUE HACE EL SISTEMA: Evalúa tu nivel de riesgo neurológico y te orienta sobre el paso más adecuado. No puede diagnosticar ni formular medicamentos. ¿Aceptas estos términos y autorizas el tratamiento de tus datos para continuar con tu teleorientación? Responde SÍ o NO. |
| --- |

| Registro obligatorio en Google Sheets al recibir SÍ |
| --- |
| consentimiento_datos        = TRUE |
| consentimiento_servicio     = TRUE |
| consentimiento_investigacion = TRUE  (incluido en el SI general) |
| timestamp_consentimiento    = 2026-03-20T10:30:00 |
| ip_o_canal                  = WhatsApp |
|  |
| Si el usuario responde NO: el agente informa que sin autorización no puede |
| continuar, ofrece el canal web https://icnsalud.com/#contacto y cierra la sesión. |

4. Esquema de Datos — Google Sheets

El sistema opera con cuatro hojas en un mismo Google Sheets. El acceso está restringido exclusivamente a cuentas institucionales de ICN Salud con autenticación de dos factores.

| Control de acceso obligatorio — Google Sheets |
| --- |
| • Solo cuentas @icnsalud.com con acceso explícito pueden ver o editar el Sheets |
| • Make accede mediante cuenta de servicio con permisos mínimos necesarios |
| • Auditoría de acceso activa (Google Workspace Admin) |
| • Sin acceso público, sin links compartidos abiertos |
| • Política de retención: datos eliminados o anonimizados a los 5 años |

4.1 Hoja 1: PACIENTES

Una fila por paciente. Clave primaria: número de teléfono WhatsApp. Se crea en F1 y se actualiza en cada fase.

| Campo | Tipo | Descripción | Ejemplo |
| --- | --- | --- | --- |
| paciente_id | Texto (auto) | ID único generado por Make | PAC-20260320-001 |
| telefono | Texto | Número WhatsApp — clave primaria | 573041234567 |
| nombre | Texto | Nombre capturado en F1 | María Torres |
| edad | Número | Edad en años | 38 |
| ciudad | Texto | Ciudad de residencia | Medellín |
| aseguramiento | Texto | Particular / Prepagada (EPS → icnsalud.com/#contacto) | Prepagada |
| entidad_prepagada | Texto | Nombre de la prepagada si aplica | Sura |
| direccion | Texto | Dirección de residencia del paciente — requerida para contexto ESRI (V2 agente) | Calle 80 # 45-12, Medellín |
| consentimiento_datos | Booleano | TRUE si autorizó tratamiento de datos en F1 | TRUE |
| consentimiento_servicio | Booleano | TRUE si aceptó términos de teleorientación | TRUE |
| consentimiento_investigacion | Booleano | TRUE si autorizó uso en investigación ICN | TRUE |
| timestamp_consentimiento | Fecha-hora | Momento exacto de aceptación del consentimiento | 2026-03-20T10:30:00 |
| fase_actual | Texto | Fase activa del agente (F0 a F6, F2.5, ADMIN, HUMANO) | F4 |
| tipo_consulta | Texto | Tipo identificado en F0: teleorientacion / agendar / reformulacion / resultados | teleorientacion |
| programa_clinico | Texto | Programa neurológico asignado | Cefalea |
| problema_seleccionado | Número (1-10) | Problema neurológico elegido por el paciente en F2 (uno por teleconsulta) | 1 |
| guia_soporte | Texto | Guía clínica que soporta la clasificación actual | ICHD-3 — Migraña sin aura G43.009 |
| cie10 | Texto | Código CIE-10 del fenotipo probable | G43.009 |
| nivel_riesgo | Texto | Bajo / Moderado / Alto / Alarma | Alto |
| score_total | Número | Puntaje acumulado del scoring F3 | 13 |
| fenotipo_probable | Texto | Fenotipo clínico probable (sin diagnóstico definitivo) | Migraña episódica de alta frecuencia |
| f25_activada | Booleano | TRUE si la fase F2.5 fue activada para este paciente | TRUE |
| apgar_score | Número (0-10) | Puntaje APGAR familiar. Vacío si F2.5 no se activó | 7 |
| apgar_clasificacion | Texto | Funcional / Disfuncion_moderada / Disfuncion_severa. Vacío si F2.5 no se activó | Funcional |
| hamilton_score | Número (0-14) | Puntaje Escala de Hamilton abreviada. Vacío si F2.5 no se activó | 6 |
| hamilton_clasificacion | Texto | Normal / Leve / Moderado / Severo. Vacío si F2.5 no se activó | Leve |
| hamilton_tipo | Texto | Depresion / Ansiedad / Mixto. Vacío si F2.5 no se activó | Ansiedad |
| flag_salud_mental | Booleano | TRUE si hamilton_clasificacion = Moderado o Severo | FALSE |
| ecomapa_notas | Texto | Síntesis conversacional del mapa familiar y ecomapa. Solo visible para equipo clínico. | Vive con esposo e hija. Red de apoyo activa. Sin conflictos familiares significativos. |
| resumen_psicosocial | Texto | Síntesis integrada de F2.5 para el reporte clínico interno | APGAR 7/funcional. Hamilton 6/ansiedad leve. Red de apoyo estable. |
| respuestas_orientacion | JSON (Texto) | Respuestas del paciente a los 6 dominios D1–D6 stringificadas | {"D1":"pulsatil","D2":"nauseas",...} |
| reporte_enviado | Booleano | TRUE si ya se envió la imagen del reporte visual | FALSE |
| conversion | Texto | Tipo de conversión lograda en F4 | Paquete diagnóstico cefalea |
| fecha_cita | Fecha | Fecha de cita agendada | 2026-03-26 |
| canal_agenda | Texto | Directo (agente) / Web (redirección) | Directo |
| estado_cita | Texto | Pendiente / Confirmada / Asistió / No asistió | Confirmada |
| fecha_primera_orientacion | Fecha | Fecha de la primera teleorientación completada | 2026-03-20 |
| fecha_ultima_orientacion | Fecha | Fecha de la última teleorientación (control cada 6 meses) | 2026-03-20 |
| cohorte | Texto | Clasificación para investigación: programa+riesgo+fenotipo | Cefalea_Alto_MigrañaFrecuente |
| requiere_humano | Booleano | TRUE si se activó escalamiento a asesor | FALSE |
| fecha_creacion | Fecha-hora | Timestamp de primer contacto | 2026-03-20T10:30:00 |
| ultima_actividad | Fecha-hora | Timestamp del último mensaje recibido | 2026-03-20T11:15:00 |
| historial_json | JSON (Texto) | Array de mensajes para contexto de ChatGPT (últimos 20 turnos) | [{role:user,...},{role:assistant,...}] |
| notas_internas | Texto | Campo libre para equipo clínico ICN | Historial familiar migraña |

4.2 Hoja 2: CONVERSACIONES

Una fila por turno. Permite auditoría completa de cada interacción y trazabilidad de decisiones clínicas.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| conv_id | Texto (auto) | ID único del turno: CONV-{paciente_id}-{timestamp} |
| paciente_id | Texto | Referencia al paciente (FK → PACIENTES) |
| telefono | Texto | Número WhatsApp (lookup rápido) |
| fase | Texto | Fase activa en ese turno (F0–F6) |
| mensaje_usuario | Texto | Mensaje exacto enviado por el paciente |
| respuesta_agente | Texto | Respuesta generada por ChatGPT y enviada al paciente |
| guia_soporte_turno | Texto | Guía clínica que soportó la decisión en ese turno específico |
| timestamp | Fecha-hora | Fecha y hora exacta del turno |
| tokens_usados | Número | Tokens consumidos en la llamada a la API de ChatGPT |
| flag_alarma | Booleano | TRUE si el turno activó una bandera roja clínica |
| escalado_humano | Booleano | TRUE si en ese turno se notificó al neuroasesor |

4.3 Hoja 3: CITAS

Una fila por cita o paquete convertido. Alimenta el seguimiento en F5.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| cita_id | Texto (auto) | ID único de la cita: CITA-{paciente_id}-{fecha} |
| paciente_id | Texto | FK → PACIENTES |
| tipo | Texto | Consulta / Paquete diagnóstico / Tratamiento |
| programa | Texto | Programa clínico asociado |
| fecha_cita | Fecha | Fecha programada |
| hora_cita | Texto | Hora programada |
| canal_agenda | Texto | Directo (agente) / Web — según ruta tomada en F4 |
| recordatorio_3d | Booleano | TRUE si ya se envió recordatorio -3 días |
| recordatorio_1d | Booleano | TRUE si ya se envió recordatorio -1 día |
| confirmacion | Texto | Pendiente / Confirmada / Cancelada |
| seguimiento_post | Booleano | TRUE si ya se realizó el seguimiento postconsulta |
| resultado_post | Texto | Medicamentos / Terapias / Exámenes ICN / Exámenes externos / Sin novedad |

4.4 Hoja 4: COHORTES_INVESTIGACION

Hoja de solo lectura para el equipo de investigación. Se alimenta automáticamente desde PACIENTES cuando se completa F3. Datos anonimizados para análisis clínico y publicaciones ICN.

| Campo | Descripción |
| --- | --- |
| cohorte_id | ID único de la entrada en investigación |
| programa_clinico | Programa neurológico evaluado |
| guia_soporte | Guía clínica base de la clasificación |
| cie10 | Código CIE-10 del fenotipo probable |
| nivel_riesgo | Bajo / Moderado / Alto / Alarma |
| fenotipo_probable | Fenotipo clínico identificado |
| score_total | Puntaje numérico total |
| respuestas_orientacion | JSON con respuestas D1–D6 (sin datos personales) |
| edad | Edad del paciente (anonimizado) |
| ciudad | Ciudad (anonimizado, solo para epidemiología) |
| fecha_evaluacion | Fecha de la teleorientación |
| conversion | ¿Se convirtió a consulta/paquete? Sí/No |
| fecha_cita | Fecha de cita si aplica (anonimizado) |

5. Flujos de Make — Escenarios de Automatización

El sistema opera con cuatro escenarios en Make. Cada uno tiene un propósito específico y se activa por un trigger diferente.

5.1 Escenario 1: Conversación principal (webhook permanente)

| Trigger: Webhook HTTP ← WhatsApp Business API |
| --- |
| Activo 24/7. Se dispara cada vez que el paciente envía un mensaje. |

| 1 | [Webhook]  Recibir mensaje de WhatsApp Parsear: numero_telefono, mensaje_texto, timestamp. Verificar firma HMAC del webhook. |
| --- | --- |

| 2 | [Google Sheets — Buscar fila]  Buscar paciente por teléfono Filtro: columna telefono = numero_recibido. Si no existe → paso 3a. Si existe → paso 3b. |
| --- | --- |

| 3a | [Google Sheets — Crear fila]  Crear nuevo paciente Insertar en PACIENTES: telefono, fecha_creacion, fase_actual=F0, historial_json=[], consentimientos=FALSE. |
| --- | --- |

| 3b | [Google Sheets — Leer fila]  Recuperar datos del paciente Obtener: fase_actual, historial_json, programa_clinico, nivel_riesgo, nombre, consentimientos, guia_soporte. |
| --- | --- |

| 4 | [Herramienta — JSON Parse]  Deserializar historial Convertir historial_json (string) a array de objetos para enviar a ChatGPT. |
| --- | --- |

| 5 | [Router — Switch]  Seleccionar system prompt por fase Según fase_actual: F0, F1, F2, F3, F4, F5, F6, ADMIN, HUMANO → cargar el prompt correspondiente. |
| --- | --- |

| 6 | [ChatGPT — Create Completion]  Llamar a GPT-4o Model: gpt-4o \| Max tokens: 800 \| Messages: [system_prompt_fase + historial + mensaje_actual]. |
| --- | --- |

| 7 | [Herramienta — JSON Parse]  Parsear respuesta JSON de IA Extraer: respuesta_visible, fase_siguiente, campos_actualizar, guia_soporte, cie10, flag_alarma, notas_internas. |
| --- | --- |

| 8 | [Google Sheets — Actualizar PACIENTES]  Actualizar datos del paciente Escribir todos los campos_actualizar + fase_actual, guia_soporte, cie10, ultima_actividad, requiere_humano. |
| --- | --- |

| 9 | [Google Sheets — Crear fila CONVERSACIONES]  Registrar turno Insertar: conv_id, paciente_id, fase, mensaje_usuario, respuesta_agente, guia_soporte_turno, timestamp, tokens, flag_alarma. |
| --- | --- |

| 10 | [Herramienta — Array + JSON]  Actualizar historial JSON Agregar turno actual al array. Si >20 turnos, eliminar el más antiguo. Stringificar. |
| --- | --- |

| 11 | [Google Sheets — Actualizar PACIENTES]  Persistir historial actualizado Escribir nuevo historial_json en campo del paciente. |
| --- | --- |

| 12 | [Router — Condicional]  Verificar fase_siguiente = ADMIN Si ADMIN → enviar mensaje con link https://icnsalud.com/#contacto y cerrar flujo. |
| --- | --- |

| 13 | [Router — Condicional]  Verificar flag_alarma Si flag_alarma = TRUE → paso 14. Si FALSE → paso 15. |
| --- | --- |

| 14 | [WhatsApp — Enviar mensaje (neuroasesor)]  Notificar escalamiento humano Enviar al número interno ICN: nombre, teléfono, síntoma de alarma, guia_soporte, resumen clínico. |
| --- | --- |

| 15 | [Router — Condicional]  Verificar si F3 completada Si fase_siguiente es F4 o F6 y reporte_enviado=FALSE → paso 16. Si no → paso 17. |
| --- | --- |

| 16 | [Escenario 2 (sub-call)]  Generar y enviar reporte visual Llamar Escenario 2 para generar imagen del reporte de riesgo y enviarla al paciente. |
| --- | --- |

| 17 | [WhatsApp — Enviar mensaje (paciente)]  Enviar respuesta al paciente Enviar respuesta_visible al número WhatsApp del paciente. |
| --- | --- |

5.2 Escenario 2: Reporte visual de riesgo

| Trigger: Llamada desde Escenario 1 (al completar F3 o F4) |
| --- |
| Genera automáticamente la imagen del reporte de riesgo y la envía por WhatsApp. |
| Incluye obligatoriamente el disclaimer legal de teleorientación. |

| 1 | [Recibir datos]  Recibir parámetros del Escenario 1 Nombre, nivel_riesgo, fenotipo_probable, programa_clinico, guia_soporte, recomendacion, cie10. |
| --- | --- |

| 2 | [Herramienta — Text Formatter]  Construir contenido del reporte Armar el texto del reporte: encabezado ICN, nombre paciente, programa, nivel de riesgo (con colores), fenotipo probable, recomendación, disclaimer legal. |
| --- | --- |

| 3 | [HTTP — POST (API de imagen)]  Generar imagen del reporte Llamar a servicio de generación de imagen (Bannerbear, imgbb, o HTML-to-image API). Pasar HTML/JSON con branding ICN. |
| --- | --- |

| 4 | [WhatsApp — Enviar imagen]  Enviar reporte visual al paciente Enviar la imagen generada con caption: 'Tu evaluación de riesgo neurológico de ICN Salud.' |
| --- | --- |

| 5 | [Google Sheets — Actualizar PACIENTES]  Marcar reporte enviado Actualizar reporte_enviado = TRUE y timestamp_reporte en hoja PACIENTES. |
| --- | --- |

| 6 | [Google Sheets — Crear fila COHORTES]  Registrar en investigación Insertar fila anonimizada en COHORTES_INVESTIGACION con todos los campos clínicos. |
| --- | --- |

5.3 Escenario 3: Recordatorios y seguimiento F5 (diario)

| Trigger: Schedule → diariamente a las 8:00 AM (UTC-5, Colombia) |
| --- |
| Revisa CITAS y envía recordatorios o seguimientos según fecha y estado. |

| 1 | [Schedule]  Trigger diario 8:00 AM Ejecutar todos los días en zona horaria Colombia (UTC-5). |
| --- | --- |

| 2 | [Google Sheets — Buscar filas]  Citas en ventana ±3 días Filtrar hoja CITAS: fecha_cita entre hoy-1 y hoy+3, estado != Asistió. |
| --- | --- |

| 3 | [Iterator]  Iterar sobre citas Procesar cada cita individualmente. |
| --- | --- |

| 4 | [Router — Condicional fecha]  Determinar tipo de acción fecha=hoy+3 y rec_3d=FALSE → recordatorio -3d. fecha=mañana y rec_1d=FALSE → confirmación. fecha=ayer y seguimiento_post=FALSE → postconsulta. |
| --- | --- |

| 5a | [WhatsApp — Enviar mensaje]  Recordatorio -3 días Mensaje con nombre, fecha/hora, programa, instrucciones de preparación y dirección/modalidad. |
| --- | --- |

| 5b | [WhatsApp — Enviar mensaje]  Confirmación -1 día Pedir SÍ o NO. Si NO → ofrecer reprogramar. Si SÍ → actualizar estado_cita=Confirmada. |
| --- | --- |

| 5c | [ChatGPT + WhatsApp]  Seguimiento postconsulta Generar con IA mensaje de seguimiento personalizado. Preguntar resultado, órdenes, siguiente paso. |
| --- | --- |

| 6 | [Google Sheets — Actualizar CITAS]  Marcar acción ejecutada Actualizar recordatorio_3d, recordatorio_1d o seguimiento_post según el caso. |
| --- | --- |

5.4 Escenario 4: Seguimiento preventivo F6 (lunes, miércoles, viernes)

| Trigger: Schedule → lunes, miércoles y viernes a las 9:00 AM |
| --- |
| Gestiona el programa educativo de Fase 6 para pacientes activos en esa fase. |

| 1 | [Schedule]  Trigger 3 veces/semana Lunes, miércoles y viernes a las 09:00 AM hora Colombia. |
| --- | --- |

| 2 | [Google Sheets — Buscar filas]  Pacientes en Fase 6 Filtrar PACIENTES: fase_actual = F6. |
| --- | --- |

| 3 | [Iterator]  Iterar por paciente Procesar individualmente. |
| --- | --- |

| 4 | [ChatGPT — Create Completion]  Generar tríada educativa personalizada Prompt F6 + programa + riesgo + historial. Generar: 1 educación breve, 1 acción concreta, 1 pregunta de seguimiento. |
| --- | --- |

| 5 | [WhatsApp — Enviar mensaje]  Enviar tríada al paciente Mensaje claro, sin tecnicismos, en tono amigable. |
| --- | --- |

| 6 | [Google Sheets — Actualizar PACIENTES]  Registrar envío Actualizar ultima_actividad. |
| --- | --- |

6. Flujo por Fases — Reglas de Operación

| Regla operativa fundamental (no negociable) |
| --- |
| El agente debe ofrecer SIEMPRE la teleorientación (F3) a TODOS los pacientes |
| una vez completada F1, sin excepción. |
|  |
| No puede saltarse F3 aunque el paciente llegue preguntando por precio o cita. |
| Esto garantiza: entrada clínica estandarizada, calidad del dato, |
| fortalecimiento de la investigación y conversión basada en riesgo real. |
|  |
| Una teleconsulta = un problema neurológico. El paciente selecciona UNO |
| de los 10 problemas disponibles en F2. Si tiene múltiples, se agenda |
| una teleconsulta separada para cada uno. |
|  |
| Si el paciente ya realizó una teleorientación previamente: |
| → Sugerir repetirla cada 6 meses como control y actualización de riesgo. |
| (Comparar con fecha_ultima_orientacion en Google Sheets) |

6.1 Tipos de consulta — F0 ampliado

En F0 el agente identifica cuál de cuatro tipos de consulta trae el paciente. Cada tipo tiene una ruta distinta.

| Tipo de consulta | Descripción | Ruta del agente | Ruta ADMIN si aplica |
| --- | --- | --- | --- |
| Teleorientación neurológica | Paciente quiere entender su problema, evaluar síntomas o requiere orientación clínica | F0 → F1 → F2 → F2.5 (condicional) → F3 → F4 → F5 → F6 | No aplica |
| Agendar una cita | Paciente quiere cita directa sin orientación previa | F0 → F1 → F2 → F3 obligatorio primero → F4 agenda | No aplica — F3 siempre antes de agenda |
| Reformulación de órdenes | Paciente necesita renovar o ajustar una orden médica existente | F0 → ADMIN_REFORMULACION | WhatsApp equipo ICN o web icnsalud.com/#contacto |
| Entrega de resultados o historia clínica | Paciente solicita resultados de exámenes o copia de historia | F0 → ADMIN_RESULTADOS | Canal administrativo ICN — no el agente |

6.2 Fase 2.5 — Evaluaciones psicosociales (condicional)

F2.5 es una fase intermedia que se activa únicamente cuando el agente detecta señales emocionales o contexto social complejo durante F1 o F2. No se aplica a todos los pacientes.

| Triggers de activación de F2.5 — señales que activan la fase |
| --- |
| El agente activa F2.5 si detecta en el historial de F1 o F2 cualquiera de: |
|  |
| SEÑALES EMOCIONALES: |
| • Menciona tristeza, llanto, desesperanza, angustia intensa o ansiedad marcada |
| • Expresa que 'ya no puede más' o frases que sugieren agotamiento emocional |
| • Menciona dificultades para dormir asociadas a preocupaciones o estrés |
| • Describe síntomas físicos con carga emocional evidente (mi dolor me tiene deprimida) |
|  |
| SEÑALES DE CONTEXTO SOCIAL COMPLEJO: |
| • Menciona vivir solo/a sin red de apoyo |
| • Describe conflictos familiares relacionados con su condición |
| • Indica dificultades económicas que afectan el acceso a atención |
| • Es cuidador principal de otro familiar enfermo |
| • Menciona pérdidas recientes (duelo, separación, desempleo) |

Evaluaciones que componen F2.5

| Herramienta | Qué mide | Cómo se aplica | Campos en Google Sheets | Guía clínica |
| --- | --- | --- | --- | --- |
| APGAR Familiar | Funcionalidad de la red familiar: Adaptabilidad, Participación, Ganancia, Afecto, Resolución | Conversacional — 5 preguntas adaptadas al tono del chat. Puntuación 0-10. 0-3: disfunción severa; 4-6: moderada; 7-10: funcional | apgar_score (0-10), apgar_clasificacion (Funcional/Disfuncion_moderada/Disfuncion_severa) | Smilkstein G. — Journal of Family Practice, 1978. Validación colombiana disponible |
| Mapa Familiar y Ecomapa | Estructura relacional del paciente y sus recursos externos (familia, trabajo, comunidad, salud) | Conversacional — el agente pregunta sobre convivencia, personas de apoyo, relación con servicios de salud. Se sintetiza en notas internas. | ecomapa_notas (texto libre con síntesis relacional) | Hanson & Mischke — Family Health Care Nursing, 1996 |
| Escala de Hamilton | Estado emocional: depresión (HDRS) y ansiedad (HARS) | Versión adaptada conversacional de 7 ítems (Hamilton abreviada). Puntuación 0-14. 0-4: normal; 5-9: leve; 10-14: moderado/severo | hamilton_score (0-14), hamilton_clasificacion (Normal/Leve/Moderado/Severo), hamilton_tipo (Depresion/Ansiedad/Mixto) | Hamilton M. — Journal of Neurology, 1960. Adaptación conversacional ICN |

| Reglas de operación de F2.5 |
| --- |
| 1. Si F2.5 NO se activa: el flujo va directo F2 → F3. |
| Los campos de F2.5 quedan vacíos en Sheets (no es error). |
|  |
| 2. Si F2.5 SÍ se activa: el agente aplica las tres herramientas en orden |
| (APGAR → Ecomapa → Hamilton) de forma conversacional, sin formato de |
| cuestionario. Máximo 2-3 preguntas por turno. |
|  |
| 3. Si hamilton_clasificacion = Moderado o Severo: |
| → Activar flag_salud_mental = TRUE |
| → El prompt de F3 recibirá este contexto y ajustará el tono |
| → En F4, la recomendación incluirá apoyo en salud mental además del programa neurológico |
| → Si hay riesgo de autolesión: fase_siguiente = HUMANO inmediatamente |
|  |
| 4. Los resultados de F2.5 se sintetizan en el campo resumen_psicosocial |
| y se incluyen en el reporte visual para el equipo clínico (no visible al paciente). |

6.3 Tabla de fases completa — V3

| Fase | Nombre | Objetivo | Entrada mínima | Salida | Condición de transición | Naturaleza |
| --- | --- | --- | --- | --- | --- | --- |
| F0 | Clasificación | Detectar tipo de consulta | Mensaje libre | tipo_consulta (teleorientacion / agendar / reformulacion / resultados) | Teleorientación/agendar → F1 \| Reformulación → ADMIN_REFORMULACION \| Resultados → ADMIN_RESULTADOS | Teleorientación |
| F1 | Identificación | Consentimiento + datos básicos + dirección | Mensaje entrante nuevo | perfil_básico completo + consentimientos = TRUE | Datos OK → F2 | Teleorientación |
| F2 | Necesidad y selección | Confirmar ruta F3 + seleccionar 1 problema neurológico | perfil_básico | problema_seleccionado (1 de 10) | Siempre → F2.5 (si señales) o F3 directo | Teleorientación |
| F2.5 | Evaluaciones psicosociales | APGAR + Ecomapa + Hamilton (condicional) | Señales emocionales o contexto social complejo detectadas | apgar_score + hamilton_score + ecomapa_notas + flag_salud_mental | Completadas → F3 | Teleorientación |
| F3 | Teleorientación clínica | Árbol clínico + scoring + reporte | 1 problema + datos básicos + contexto F2.5 si aplica | nivel_riesgo + fenotipo + CIE-10 + reporte visual | Bajo → F6 \| Mod/Alto → F4 \| Alarma → HUMANO | Teleorientación |
| F4 | Conversión | Agenda + paquete diagnóstico | Riesgo + programa + agenda disponible | conversión o escalado | Acepta → F5 \| Rechaza → F6 \| Humano → HUMANO | Teleorientación comercial |
| F5 | Seguimiento | Recordatorios + postconsulta | Cita convertida + fecha | asistencia + resultado_post | Postconsulta → F6 o F4 | Teleorientación |
| F6 | Prevención | Educación + remarketing + investigación | nivel_riesgo + programa | adherencia + señales de reactivación | Síntoma nuevo → F3 \| Interés → F4 \| Alarma → HUMANO | Teleorientación |
| ADMIN_REFORMULACION | Admin — Órdenes | Gestionar reformulación | Solicitud de reforma de orden | Contacto con equipo ICN | Fin en agente | Administrativo |
| ADMIN_RESULTADOS | Admin — Resultados/HC | Gestionar entrega de documentos | Solicitud de resultado o HC | Canal administrativo ICN | Fin en agente | Administrativo |
| HUMANO | Escalamiento | Transferir a neuroasesor | Alarma / solicitud / duda / hamilton severo | Notificación equipo ICN | Fin en agente | Puede ser Telemedicina |

7. Integración de Agenda — Pacientes Particulares (F4)

Acordado con Jeneth: se habilitarán bloques específicos de agenda para pacientes particulares. El agente puede agendar directamente o redirigir a la web según la disponibilidad.

7.1 Flujo de agenda en F4

| Lógica de agenda en Fase 4 |
| --- |
| Cuando el paciente acepta agendar en F4: |
|  |
| 1. Make consulta disponibilidad en Google Calendar / Calendly (API) |
| Filtro: bloques habilitados para particulares |
|  |
| 2. Si hay disponibilidad en las próximas 72h: |
| → El agente ofrece 2-3 opciones de horario directamente en el chat |
| → El paciente elige y Make confirma la cita automáticamente |
| → Se crea fila en hoja CITAS con canal_agenda = 'Directo' |
|  |
| 3. Si NO hay disponibilidad inmediata o el sistema no puede confirmar: |
| → El agente redirige: 'Puedes agendar directamente en icnsalud.com' |
| → Se registra canal_agenda = 'Web' en CITAS |
|  |
| 4. En ambos casos: Make crea fila en CITAS y activa el Escenario 3 (F5). |

7.2 Requisitos técnicos de la integración

| Componente | Configuración necesaria | Responsable |
| --- | --- | --- |
| Google Calendar o Calendly | Crear calendario específico para particulares. Definir bloques disponibles con Jeneth. Conectar API en Make. | ICN (Jeneth) + Técnico |
| Make — módulo Calendar | Módulo 'List Events' o 'Create Event' de Google Calendar / Calendly. Filtrar por tipo de paciente = Particular. | Técnico Make |
| Manejo de conflictos | Si el slot se toma entre que el agente lo ofrece y el paciente confirma: ofrecer alternativa automáticamente. | Técnico Make |
| Notificación al equipo | Cuando se confirma cita directa: Make envía notificación al equipo ICN (WhatsApp o email). | Técnico Make |

7B. Integración ESRI — Contexto de Vida por Dirección (Roadmap V2 agente)

| Estado: Planificado para V2 del agente — no incluir en implementación inicial |
| --- |
| La integración con ESRI (https://www.esri.co/es-co/home) permite que el agente |
| consulte automáticamente condiciones sociodemográficas y ambientales del entorno |
| del paciente a partir de su dirección de residencia. |
|  |
| Esto enriquece el perfil clínico con variables contextuales que pueden |
| influir en el riesgo neurológico: estrato socioeconómico, acceso a servicios, |
| contaminación ambiental, densidad poblacional, condiciones de vivienda. |

7B.1 Datos que aportaría ESRI al perfil del paciente

| Variable ESRI | Relevancia clínica | Campo en Google Sheets (V2) |
| --- | --- | --- |
| Estrato socioeconómico | Acceso a medicamentos, alimentación, estrés crónico | esri_estrato |
| Índice de calidad de vida urbana | Condiciones de vivienda, hacinamiento, saneamiento | esri_calidad_vida |
| Proximidad a zonas de contaminación | Factor de riesgo para cefalea, ACV, neuropatías | esri_contaminacion |
| Acceso a servicios de salud en radio 2km | Determina facilidad de seguimiento presencial | esri_acceso_salud |
| Cobertura de internet / conectividad | Relevante para telemedicina de seguimiento | esri_conectividad |
| Zona de conflicto o vulnerabilidad | Factor de estrés crónico y salud mental | esri_vulnerabilidad |

7B.2 Implementación técnica en Make (V2)

| Flujo de integración ESRI en Make — Escenario 1 ampliado |
| --- |
| REQUISITO PREVIO: capturar campo direccion en F1 (ya incluido en V3 del esquema). |
|  |
| Paso nuevo en Escenario 1 (después de paso 3b — leer datos del paciente): |
| Si esri_consultado = FALSE y direccion != vacío: |
| → HTTP GET a API de ESRI con dirección del paciente |
| → Parsear respuesta: estrato, índices, proximidades |
| → Actualizar campos esri_* en PACIENTES |
| → Incluir resumen ESRI en el system prompt de F2.5 y F3 |
| → esri_consultado = TRUE (no volver a consultar en sesiones futuras) |
|  |
| El resumen ESRI se incluye en notas_internas del reporte clínico, |
| no en la respuesta visible al paciente. |

8. Prompts de ChatGPT por Fase

Todos los prompts usan el formato JSON estructurado para que Make procese las respuestas automáticamente. El lenguaje de teleorientación es obligatorio en todos.

| Formato JSON obligatorio de respuesta — Todas las fases |
| --- |
| { |
| "respuesta_visible": "Texto que se enviará al paciente por WhatsApp", |
| "fase_siguiente": "F0\|F1\|F2\|F3\|F4\|F5\|F6\|ADMIN\|HUMANO", |
| "campos_actualizar": { }, |
| "guia_soporte": "ICHD-3 criterio X / DSM-5-TR criterio Y / Guía ICN", |
| "cie10": "G43.009", |
| "flag_alarma": false, |
| "notas_internas": "Texto solo visible para equipo clínico ICN" |
| } |
|  |
| guia_soporte y cie10 son obligatorios solo cuando se completa F3. |
| flag_alarma = true activa escalamiento inmediato a neuroasesor humano. |

8.1 Prompt base del sistema (incluir en todas las fases)

| SYSTEM PROMPT BASE Eres NeurOrientador, el sistema de teleorientación neurológica de ICN Salud. Tu rol es orientar a los pacientes mediante una evaluación estructurada de riesgo neurológico. Eres amable, empático y profesional. REGLAS ABSOLUTAS E INNEGOCIABLES: 1. Responde SIEMPRE en formato JSON válido (estructura definida). 2. NUNCA emitas diagnóstico definitivo. Lenguaje obligatorio: 'Esto sugiere un nivel de riesgo...' / 'El especialista podrá confirmar...' 3. NUNCA formules medicamentos ni recomiendes dosis. 4. SIEMPRE escala a HUMANO si detectas: pensamiento suicida, dolor torácico, pérdida de consciencia, convulsión activa, ACV probable (FAST positivo), cefalea en trueno, fiebre + rigidez de nuca. 5. SIEMPRE presenta el servicio como teleorientación, no como consulta médica. 6. Todos los pacientes deben pasar por F3 (teleorientación), sin excepción. Datos actuales del paciente: - Nombre: {{nombre}} \| Edad: {{edad}} \| Ciudad: {{ciudad}} - Aseguramiento: {{aseguramiento}} \| Fase: {{fase_actual}} - Programa: {{programa_clinico}} \| Riesgo previo: {{nivel_riesgo}} - Última orientación: {{fecha_ultima_orientacion}} |
| --- |

8.2 Prompt Fase 0 — Clasificación inicial

| PROMPT F0 {{SYSTEM_PROMPT_BASE}} FASE: F0 — Clasificar intención del primer mensaje. REGLAS: - Síntomas neurológicos / interés clínico / precio / cita → fase_siguiente: F1 - EPS / autorización / historia clínica / admin → fase_siguiente: ADMIN (En ADMIN: respuesta_visible debe incluir link https://icnsalud.com/#contacto) - Prepagada / particular → fase_siguiente: F1 En respuesta_visible: saludo breve ICN Salud. |
| --- |

8.3 Prompt Fase 1 — Consentimiento e identificación

| PROMPT F1 {{SYSTEM_PROMPT_BASE}} FASE: F1 — Consentimiento informado + datos básicos. PASO 1 — Si consentimiento_datos = FALSE: Enviar el mensaje completo de consentimiento (Ley 1581/2012, naturaleza del servicio, uso en investigación). Esperar SÍ o NO. Si NO: respuesta_visible con info de https://icnsalud.com/#contacto. Si SÍ: campos_actualizar = {consentimiento_datos:true, consentimiento_servicio:true, consentimiento_investigacion:true, timestamp_consentimiento: [ahora]} PASO 2 — Una vez consintió: capturar nombre, edad, ciudad, aseguramiento. Si EPS: respuesta_visible con link icnsalud.com/#contacto, fase_siguiente: ADMIN. Si Prepagada: solicitar nombre de la entidad y foto de orden si existe. MÁXIMO 2 preguntas por turno. NO hacer preguntas clínicas aquí. PASO 3 — Si nombre+edad+ciudad+aseguramiento completos: Mostrar brevemente los programas disponibles. Preguntar cuál describe mejor su situación. fase_siguiente: F2 Si paciente ya hizo orientación antes (fecha_ultima_orientacion no vacía y han pasado >6 meses): mencionar que se recomienda actualizar la evaluación. |
| --- |

8.4 Prompt Fase 2 — Selección de problema neurológico

| PROMPT F2 {{SYSTEM_PROMPT_BASE}} FASE: F2 — Seleccionar problema neurológico y confirmar ruta F3. REGLA: Todos los pacientes pasan por F3. Una teleconsulta = UN problema. Si el paciente pide precio o cita: explicar que primero se hace la evaluación de riesgo para orientarlo mejor. PASO 1 — Presentar los 10 problemas disponibles: 1. Dolor de cabeza 2. Convulsiones 3. Retraso en neurodesarrollo 4. Temblores y movimientos anormales 5. Problemas de sueño 6. Problemas de memoria 7. Accidente cerebrovascular (ACV) 8. Parálisis facial 9. Dolores crónicos 10. Problemas neuromusculares PASO 2 — Si el paciente no tiene claro cuál elegir: Ayudar con preguntas clarificadoras sin sesgar la decisión. Ej: '¿El principal problema es el dolor, o más bien los movimientos?' PASO 3 — Si menciona múltiples problemas: 'Podemos evaluar un problema por teleconsulta. ¿Cuál le afecta más hoy?' Registrar los otros problemas en notas_internas para teleconsultas futuras. PASO 4 — Antes de ir a F3, evaluar si activar F2.5: Revisar el historial de F1 y F2 buscando señales emocionales o sociales (ver lista de triggers en el documento técnico). Si hay señales → fase_siguiente: F2.5 Si no hay señales → fase_siguiente: F3 campos_actualizar: {problema_seleccionado: número, programa_clinico: nombre} |
| --- |

8.5 Prompt Fase 2.5 — Evaluaciones psicosociales (condicional)

| PROMPT F2.5 — Solo se activa si se detectaron señales en F1 o F2 {{SYSTEM_PROMPT_BASE}} FASE: F2.5 — Evaluaciones psicosociales antes de la teleorientación clínica. Esta fase se aplica SOLO porque se detectaron señales emocionales o de contexto social complejo. El paciente NO sabe que está en una 'evaluación'. TONO: Muy empático, conversacional, nunca clínico-frío. Validar antes de preguntar. MÁXIMO 2 preguntas por turno. Total de la fase: máximo 4-5 turnos. SECUENCIA: 1. APGAR FAMILIAR (5 preguntas conversacionales, adaptadas al contexto): A — '¿Siente que su familia le apoya cuando tiene dificultades de salud?' P — '¿Puede hablar con su familia sobre sus preocupaciones?' G — '¿Siente que su familia acepta y respeta sus decisiones?' A — '¿Siente afecto y amor de parte de su familia?' R — '¿Su familia y usted se ayudan mutuamente en los momentos difíciles?' Cada respuesta: Siempre=2, A veces=1, Nunca=0. Sumar → 0-10. 2. ECOMAPA (síntesis conversacional — no es cuestionario): '¿Con quién vive actualmente?' / '¿Tiene personas cercanas en quien apoyarse?' '¿Trabaja actualmente?' / '¿Pertenece a algún grupo o comunidad?' Sintetizar en ecomapa_notas (texto libre para equipo clínico). 3. HAMILTON ABREVIADO (7 ítems conversacionales, 0-2 cada uno, máx 14): 'En las últimas dos semanas, ¿cómo ha estado su ánimo en general?' '¿Ha tenido momentos de tristeza intensa o ganas de llorar?' '¿Ha sentido mucha preocupación o nerviosismo sin razón clara?' '¿Ha tenido dificultad para dormir por pensamientos o angustia?' '¿Ha perdido el interés en cosas que antes le gustaban?' '¿Ha sentido tensión muscular, palpitaciones o sensación de ahogo?' '¿Ha podido hacer sus actividades diarias con normalidad?' 0-4: Normal \| 5-9: Leve \| 10-14: Moderado/Severo AL COMPLETAR F2.5: Si hamilton_score >= 10 (Moderado/Severo): campos_actualizar = {flag_salud_mental: true} Incluir en respuesta_visible: validación empática + mencionar que el equipo ICN también cuenta con apoyo en salud mental. Si hay riesgo de autolesión → fase_siguiente: HUMANO inmediatamente. Si hamilton_score < 10: fase_siguiente: F3 Siempre incluir en campos_actualizar: {apgar_score, apgar_clasificacion, hamilton_score, hamilton_clasificacion, hamilton_tipo, flag_salud_mental, ecomapa_notas, resumen_psicosocial, f25_activada: true} |
| --- |

8.6 Prompt Fase 3 — Teleorientación neurológica

| PROMPT F3 — NÚCLEO CLÍNICO (ejemplo: programa Cefalea / ICHD-3) {{SYSTEM_PROMPT_BASE}} FASE: F3 — Teleorientación neurológica estructurada. Programa: {{programa_clinico}} \| Problema seleccionado: {{problema_seleccionado}} Score acumulado: {{score_total}} Guía base: ICHD-3 (Cefalea) \| Adaptar guía según programa activo. CONTEXTO PSICOSOCIAL (de F2.5 si fue activada): flag_salud_mental: {{flag_salud_mental}} hamilton_clasificacion: {{hamilton_clasificacion}} apgar_clasificacion: {{apgar_clasificacion}} resumen_psicosocial: {{resumen_psicosocial}} Si flag_salud_mental = TRUE: ajustar el tono a mayor calidez y validación emocional en cada respuesta. Mencionar brevemente el apoyo de salud mental de ICN al presentar la recomendación en F4. ÁRBOL CONVERSACIONAL — 6 DOMINIOS (1-2 preguntas por turno máximo): D1 CONFIRMACIÓN (mapea ICHD-3 Criterio B — características del dolor): '¿El dolor es pulsátil o en presión? ¿En qué zona?' Score: pulsátil unilateral +2 \| bilateral/presión +1 \| otro +0 D2 ALARMA (banderas rojas — escalar inmediatamente si presentes): '¿Ha tenido fiebre, vómito en proyectil, visión doble, pérdida de fuerza, el peor dolor de su vida de inicio súbito, rigidez en la nuca?' Score: ninguno +0 \| uno +1 \| DOS O MÁS → flag_alarma: true D3 CARACTERIZACIÓN (mapea ICHD-3 Criterio A — frecuencia y duración): '¿Cuántas veces por semana/mes? ¿Desde hace cuánto?' Score: <1/semana +1 \| 1-2/semana +2 \| ≥3/semana o crónico +3 D4 SEVERIDAD (mapea ICHD-3 Criterio C — intensidad y limitación): '¿Del 0 al 10 cuánto le afecta la vida diaria?' Score: 1-4 +1 \| 5-7 +2 \| 8-10 +3 D5 FENOTIPO (mapea ICHD-3 Criterio C — síntomas asociados): '¿Sensibilidad a luz, ruido, náuseas, aura visual?' Score: uno +1 \| dos +2 \| tres o más +3 D6 SALIDA (historial de tratamiento y comorbilidades): '¿Ha tomado medicamento? ¿Con qué resultado?' Score: sin medicamento/sin efecto +3 \| efecto parcial +2 \| buen control +1 CLASIFICACIÓN FINAL (score máximo 15): 0-4: Bajo → fase_siguiente: F6 5-8: Moderado → fase_siguiente: F4 9-12: Alto → fase_siguiente: F4 13-15 o flag_alarma=true: Alarma → fase_siguiente: HUMANO Al completar los 6 dominios, incluir en campos_actualizar: score_total, nivel_riesgo, fenotipo_probable, guia_soporte (ej: 'ICHD-3 G43.009 — Migraña episódica de alta frecuencia'), cie10, respuestas_orientacion (JSON con D1-D6), fecha_ultima_orientacion. En respuesta_visible usar lenguaje de teleorientación SIEMPRE: 'Esto sugiere un nivel de riesgo neurológico...' 'El especialista podrá confirmar...' NUNCA decir: 'Tienes X' / 'Tu diagnóstico es X'. |
| --- |

8.7 Prompt Fase 4 — Conversión clínica

| PROMPT F4 {{SYSTEM_PROMPT_BASE}} FASE: F4 — Conversión clínica y comercial. Riesgo: {{nivel_riesgo}} \| Fenotipo: {{fenotipo_probable}} \| CIE-10: {{cie10}} ESTRUCTURA DE CONVERSACIÓN F4: T1: Resumir hallazgos de la teleorientación con lenguaje prudente. Explicar por qué amerita evaluación especializada. T2: Presentar paquete diagnóstico del programa. Mencionar qué incluye. T3: Si hay objeción → manejarla (ver abajo). Si pregunta por agenda → consultar disponibilidad (Escenario 1 llama Google Calendar/Calendly). T4: Ofrecer 2-3 opciones de horario o redirigir a icnsalud.com si no hay. MANEJO DE OBJECIONES: 'Es caro' → costo de tratamiento tardío vs. valor del diagnóstico temprano 'Ya fui al médico' → valor del especialista neurólogo vs. médico general 'Tengo miedo' → validar, normalizar, enfocar en solución 'Quiero pensarlo' → respetar, ofrecer info adicional, acordar seguimiento 'Soy EPS' → redirigir a icnsalud.com/#contacto Si paciente pide humano → fase_siguiente: HUMANO Si acepta agenda directa → campos_actualizar={conversion:...,canal_agenda:'Directo'} Si se redirige a web → campos_actualizar={canal_agenda:'Web'} En ambos casos → fase_siguiente: F5 Si rechaza completamente → fase_siguiente: F6 |
| --- |

8.8 Prompt Fase 6 — Prevención, educación e investigación

| PROMPT F6 {{SYSTEM_PROMPT_BASE}} FASE: F6 — Seguimiento preventivo, educación y remarketing. Programa: {{programa_clinico}} \| Riesgo: {{nivel_riesgo}} Última orientación: {{fecha_ultima_orientacion}} Enviar la TRÍADA de seguimiento (máximo 4 líneas en total, lenguaje sencillo): 1. EDUCACIÓN: Un dato útil relacionado con el programa del paciente. 2. ACCIÓN: Una recomendación concreta que pueda hacer hoy. 3. PREGUNTA: Una pregunta simple de seguimiento de evolución. Contenido por programa: Cefalea: hidratación, sueño, manejo de estrés, diario de migraña Epilepsia: adherencia, sueño regular, evitar triggers, seguridad Sueño: higiene del sueño, horarios, cafeína, pantallas Memoria: estimulación cognitiva, actividad física, socialización ESCALAMIENTO DESDE F6: Síntomas empeoran → fase_siguiente: F3 Pregunta por consulta/paquete → fase_siguiente: F4 Angustia emocional intensa → fase_siguiente: HUMANO Han pasado ≥6 meses desde fecha_ultima_orientacion → sugerir actualizar la teleorientación, fase_siguiente: F3 |
| --- |

9. Simulación del Proceso Completo de Atención

Paciente: María Torres, 38 años, Medellín, Prepagada Sura. Motivo: dolores de cabeza frecuentes e intensos que le impiden trabajar.

|  | Turno 1  [F0 → F1] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Hola buenas, me han recomendado este número. Tengo unos dolores de cabeza muy fuertes que no me dejan trabajar. |  |
| Agente: |  | Hola, bienvenida a ICN Salud. Soy NeurOrientador, el sistema de teleorientación neurológica de ICN Salud. Con gusto te orientamos. Antes de comenzar necesito compartirte información importante sobre nuestro servicio. |  |
| Make: |  | Make crea fila nueva en PACIENTES: telefono=573041234567, fase_actual=F0. Escenario 1 paso 3a ejecutado. |  |
| Sheets: |  | PACIENTES: nueva fila creada. fase_actual=F0. consentimientos=FALSE. |  |
|  |  |  |  |

|  | Turno 2  [F1 — Consentimiento] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | [Paciente lee el mensaje] |  |
| Agente: |  | Antes de comenzar, te informo: (1) Tus datos se tratan con confidencialidad según la Ley 1581/2012. (2) Este es un servicio de TELEORIENTACIÓN, no una consulta médica — el resultado es una evaluación de riesgo, no un diagnóstico. (3) Tus datos anonimizados podrán usarse en investigación clínica ICN. ¿Aceptas estos términos? Responde SÍ o NO. |  |
| Make: |  | ChatGPT detecta paciente nuevo sin consentimiento. Genera mensaje de consentimiento completo. fase_actual=F1. |  |
| Sheets: |  | PACIENTES: fase_actual=F1. |  |
|  |  |  |  |

|  | Turno 3  [F1 — Datos básicos] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Sí, acepto. |  |
| Agente: |  | Perfecto, gracias. Para orientarte mejor necesito algunos datos: ¿cuál es tu nombre completo, tu edad y tu ciudad? |  |
| Make: |  | campos_actualizar={consentimiento_datos:true, consentimiento_servicio:true, consentimiento_investigacion:true, timestamp_consentimiento:2026-03-20T10:32:00}. |  |
| Sheets: |  | PACIENTES: todos los consentimientos=TRUE. timestamp_consentimiento registrado. |  |
|  |  |  |  |

|  | Turno 4  [F1 — Aseguramiento] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | María Torres, 38 años, Medellín. |  |
| Agente: |  | Mucho gusto, María. ¿Tienes medicina prepagada o pagas de forma particular? |  |
| Make: |  | campos_actualizar={nombre:'María Torres', edad:38, ciudad:'Medellín'}. |  |
| Sheets: |  | PACIENTES: nombre, edad, ciudad actualizados. |  |
|  |  |  |  |

|  | Turno 5  [F1 → F2 → F3] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Prepagada Sura. |  |
| Agente: |  | Perfecto. Atendemos programas de Cefalea, Epilepsia, Sueño, Memoria y más. Dado lo que mencionas, comenzaremos con la evaluación de riesgo neurológico para cefalea — esto nos permitirá orientarte de la mejor forma. ¿Comenzamos? |  |
| Make: |  | campos_actualizar={aseguramiento:'Prepagada', entidad_prepagada:'Sura', programa_clinico:'Cefalea', fase_actual:'F3'}. EPS habría generado fase_siguiente=ADMIN con link. |  |
| Sheets: |  | PACIENTES: aseguramiento=Prepagada, programa_clinico=Cefalea, fase_actual=F3. |  |
|  |  |  |  |

|  | Turno 6  [F3 — D1 + D2] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Sí, claro. |  |
| Agente: |  | Gracias. Primer grupo de preguntas: ¿El dolor es pulsátil (como latidos) o sientes una presión constante? ¿Y en qué zona de la cabeza lo sientes principalmente? |  |
| Make: |  | F3 iniciada. Dominio D1 activado. score_total=0 hasta respuesta. |  |
| Sheets: |  | PACIENTES: sin cambios aún en score. |  |
|  |  |  |  |

|  | Turno 7  [F3 — D1 ✓, D2] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Es pulsátil, en el lado derecho. A veces me da náuseas también. |  |
| Agente: |  | Entiendo. ¿Ha tenido junto con estos dolores: fiebre, vómito en proyectil, visión doble, pérdida de fuerza o el peor dolor de su vida de inicio súbito? |  |
| Make: |  | D1=+2 (pulsátil unilateral, ICHD-3 Criterio B). D2 activado. campos_actualizar={score_total:2, respuestas_orientacion:{D1:'pulsatil_derecho', D2:'pendiente'}}. |  |
| Sheets: |  | PACIENTES: score_total=2. |  |
|  |  |  |  |

|  | Turno 8  [F3 — D2 ✓, D3] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | No, nada de eso. Solo las náuseas. |  |
| Agente: |  | Bien. ¿Cuántas veces a la semana le dan estos dolores aproximadamente? ¿Y desde hace cuánto tiempo tiene este problema? |  |
| Make: |  | D2=+1 (náuseas, sin banderas rojas). score_total=3. flag_alarma=false. D3 activado. |  |
| Sheets: |  | PACIENTES: score_total=3. flag_alarma=false. |  |
|  |  |  |  |

|  | Turno 9  [F3 — D3 ✓, D4] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Unas 3 o 4 veces a la semana, llevo como 3 meses así. |  |
| Agente: |  | Eso es bastante frecuente y entiendo lo difícil que debe ser. Del 0 al 10, ¿qué tanto le afectan estos dolores en su vida diaria — trabajo, actividades, descanso? |  |
| Make: |  | D3=+3 (≥3/semana, 3 meses — ICHD-3 Criterio A: >15 días/mes en el umbral). score_total=6. |  |
| Sheets: |  | PACIENTES: score_total=6. |  |
|  |  |  |  |

|  | Turno 10  [F3 — D4 ✓, D5] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Un 7, hay días que no puedo ni trabajar. |  |
| Agente: |  | Entiendo. Cuando tiene el dolor, ¿es sensible a la luz brillante o a los ruidos fuertes? |  |
| Make: |  | D4=+3 (7/10, limitación laboral — ICHD-3 Criterio C: agravación con actividad). score_total=9. |  |
| Sheets: |  | PACIENTES: score_total=9. |  |
|  |  |  |  |

|  | Turno 11  [F3 — D5 ✓, D6] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Sí, a los dos. Tengo que cerrar las persianas y todo. |  |
| Agente: |  | ¿Ha tomado algún medicamento para estos dolores? ¿Le ha funcionado bien? |  |
| Make: |  | D5=+2 (fotofobia + fonofobia — ICHD-3 Criterio C). score_total=11. |  |
| Sheets: |  | PACIENTES: score_total=11. |  |
|  |  |  |  |

|  | Turno 12 — CLASIFICACIÓN  [F3 → F4 + Reporte visual] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Solo ibuprofeno pero casi no me hace nada. |  |
| Agente: |  | María, gracias por toda la información. Con base en tu evaluación de riesgo, esto sugiere un nivel de RIESGO ALTO neurológico, compatible con migraña episódica de alta frecuencia. El especialista neurólogo podrá confirmar y definir el manejo más adecuado. En un momento recibirás tu reporte de evaluación. ¿Te cuento sobre las opciones de seguimiento? |  |
| Make: |  | D6=+2 (ibuprofeno sin efecto). score_total=13. nivel_riesgo=Alto. fenotipo='Migraña episódica alta frecuencia'. guia_soporte='ICHD-3 G43.009'. cie10='G43.009'. Escenario 2 activado → genera imagen reporte → envía por WhatsApp. Fila insertada en COHORTES_INVESTIGACION. |  |
| Sheets: |  | PACIENTES: score_total=13, nivel_riesgo=Alto, guia_soporte=ICHD-3, cie10=G43.009, reporte_enviado=TRUE, fecha_ultima_orientacion=2026-03-20. COHORTES: nueva fila anonimizada. |  |
|  |  |  |  |

|  | Turno 13 — REPORTE VISUAL  [F3 — Imagen automática] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | [Recibe imagen del reporte] |  |
| Agente: |  | [IMAGEN: Reporte de Evaluación de Riesgo Neurológico ICN Salud — Programa: Cefalea — Nivel de riesgo: ALTO — Fenotipo probable: Migraña episódica de alta frecuencia — Recomendación: Evaluación con especialista neurólogo — AVISO: Este resultado corresponde a una evaluación de riesgo y no constituye un diagnóstico médico] |  |
| Make: |  | Escenario 2 completado. Imagen generada con branding ICN + disclaimer legal. reporte_enviado=TRUE. |  |
| Sheets: |  | PACIENTES: reporte_enviado=TRUE. |  |
|  |  |  |  |

|  | Turno 14 — CONVERSIÓN  [F4 → F5] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Sí, cuéntame. ¿Cuánto vale? |  |
| Agente: |  | El Paquete Diagnóstico de Cefalea incluye consulta con neurólogo especialista y valoración completa. María, llevas 3 meses con dolores que te limitan el trabajo — una evaluación temprana evita que el problema avance. Tenemos disponibilidad esta semana. ¿Te quedaría bien el jueves o el viernes? |  |
| Make: |  | F4 activada. Objeción de precio manejada con argumento clínico. Make consulta Google Calendar → slots disponibles jueves y viernes. campos_actualizar={conversion:'Paquete cefalea', canal_agenda:'Directo', fase_actual:'F5'}. Nueva fila en CITAS. |  |
| Sheets: |  | PACIENTES: conversion=Paquete cefalea, canal_agenda=Directo, fase_actual=F5. CITAS: nueva fila con fecha pendiente confirmación. |  |
|  |  |  |  |

9.1 Estado final en Google Sheets

| Hoja | Campo | Valor final |
| --- | --- | --- |
| PACIENTES | nombre | María Torres |
| PACIENTES | aseguramiento | Prepagada — Sura |
| PACIENTES | consentimientos | TRUE (datos + servicio + investigación) |
| PACIENTES | fase_actual | F5 |
| PACIENTES | programa_clinico | Cefalea |
| PACIENTES | guia_soporte | ICHD-3 — G43.009 Migraña episódica alta frecuencia |
| PACIENTES | cie10 | G43.009 |
| PACIENTES | nivel_riesgo | Alto |
| PACIENTES | score_total | 13 |
| PACIENTES | fenotipo_probable | Migraña episódica de alta frecuencia |
| PACIENTES | respuestas_orientacion | JSON D1–D6 guardado |
| PACIENTES | reporte_enviado | TRUE |
| PACIENTES | conversion | Paquete diagnóstico cefalea |
| PACIENTES | canal_agenda | Directo |
| PACIENTES | fecha_ultima_orientacion | 2026-03-20 |
| PACIENTES | cohorte | Cefalea_Alto_MigrañaFrecuente |
| CONVERSACIONES | turnos registrados | 14 turnos con guia_soporte por turno |
| CITAS | estado | Pendiente confirmación de fecha |
| COHORTES_INVESTIGACION | fila anonimizada | Insertada con todos los campos clínicos |

10. Capa de Investigación Clínica

NeurOrientador no es solo un flujo conversacional. Está estructurado como un sistema de recolección de evidencia clínica propia de ICN Salud. Esta capa permite análisis longitudinal, identificación de patrones y base para publicaciones científicas.

10.1 Variables clínicas estructuradas recolectadas

| Variable | Fuente | Tipo | Uso en investigación |
| --- | --- | --- | --- |
| Programa clínico | F1 — selección paciente | Categórica | Segmentación de cohortes por área neurológica |
| Nivel de riesgo | F3 — scoring | Ordinal (Bajo/Mod/Alto/Alarma) | Distribución de riesgo poblacional ICN |
| Score total | F3 — suma D1-D6 | Numérica continua | Análisis de correlación con desenlaces |
| Fenotipo probable | F3 — clasificación | Categórica | Prevalencia de fenotipos por programa |
| CIE-10 | F3 — asignación automática | Código estandarizado | Interoperabilidad con sistemas de salud |
| Guía soporte | F3 — trazabilidad | Texto estructurado | Auditoría metodológica y validación |
| Respuestas D1–D6 | F3 — árbol completo | JSON estructurado | Análisis de patrones de síntomas |
| Tiempo F1 → conversión | Timestamp F1 vs. F4 | Numérica (días) | Optimización del embudo de conversión |
| Adherencia F5–F6 | Respuestas a recordatorios | Booleana por turno | Tasa de seguimiento y adherencia |
| Reorientación cada 6 meses | fecha_ultima_orientacion | Fecha | Seguimiento longitudinal de evolución de riesgo |

10.2 Clasificación automática por cohortes

| Formato del campo cohorte (autogenerado por Make al completar F3) |
| --- |
| Estructura: {programa}_{riesgo}_{fenotipo_abreviado} |
|  |
| Ejemplos: |
| Cefalea_Alto_MigrañaFrecuente |
| Epilepsia_Moderado_CrisisGeneralizada |
| Sueño_Bajo_InsomnioLeve |
| Neurodesarrollo_Alto_TDAH |
|  |
| Este campo permite filtrar y analizar cohortes directamente en Google Sheets |
| sin procesamiento adicional. Es la base para los análisis de investigación ICN. |

10.3 Resultados esperados de la capa de investigación

•        Evidencia clínica propia ICN: datos reales de pacientes colombianos con validación metodológica (ICHD-3, DSM-5-TR, Guías ICN).

•        Optimización de protocolos: identificación de preguntas con mayor valor predictivo para ajustar el árbol clínico de F3.

•        Base para publicaciones científicas: cohortes estructuradas con CIE-10, guía soporte y seguimiento longitudinal.

•        Análisis con IA (V2): módulo de ChatGPT sobre COHORTES_INVESTIGACION para identificar patrones y optimizar rutas clínicas automáticamente.

11. Reporte Visual de Riesgo — Entrega al Paciente

Al finalizar F3 (o al transitar a F4), el sistema genera automáticamente una imagen de reporte clínico y la envía por WhatsApp. Este reporte es obligatorio y no puede omitirse.

11.1 Contenido obligatorio del reporte visual

| Elemento | Contenido | Obligatorio |
| --- | --- | --- |
| Encabezado | Logo ICN Salud + nombre 'NeurOrientador' + fecha de evaluación | Sí |
| Nombre del paciente | Nombre capturado en F1 | Sí |
| Programa evaluado | Nombre del programa clínico (ej: Cefalea) | Sí |
| Nivel de riesgo | Bajo / Moderado / Alto / Alarma — con color indicador | Sí |
| Fenotipo probable | Descripción del fenotipo (sin diagnóstico definitivo) | Sí |
| Guía base | Guía clínica que soportó la clasificación | Sí |
| Recomendación | Paso siguiente recomendado (consulta especialista) | Sí |
| Disclaimer legal | 'Este resultado corresponde a una evaluación de riesgo y no constituye un diagnóstico médico' — texto completo obligatorio | Sí — nunca puede omitirse |
| Pie de página | ICN Salud + Teleorientación en Salud Neurológica + contacto | Sí |

11.2 Implementación técnica del reporte

| Opciones de implementación para generación de imagen en Make |
| --- |
| OPCIÓN A — Bannerbear API (recomendada para V1): |
| Crear template en Bannerbear con branding ICN. |
| Make llama a la API de Bannerbear con los datos del paciente. |
| Bannerbear genera la imagen y devuelve URL. |
| Make envía la imagen por WhatsApp usando la URL. |
|  |
| OPCIÓN B — HTML-to-Image API (más flexible): |
| Make construye un HTML con los datos del paciente. |
| Llama a una API de HTML-to-image (ej: hcti.io, htmlcsstoimage). |
| Obtiene la URL de la imagen generada. |
| Envía por WhatsApp. |
|  |
| OPCIÓN C — Google Slides/Docs API (integración nativa Google): |
| Template en Google Slides. Make llena los campos con datos. |
| Exporta como imagen PNG. Envía por WhatsApp. |
|  |
| En todos los casos: el disclaimer legal es un texto fijo no editable. |

12. Escalamiento Obligatorio a Humano

El escalamiento a neuroasesor humano es obligatorio en los siguientes casos. Make ejecuta la notificación automáticamente cuando flag_alarma = TRUE o fase_siguiente = HUMANO.

| Trigger | Descripción | Acción de Make | Mensaje al paciente |
| --- | --- | --- | --- |
| Signo de alarma clínica | ChatGPT detecta: cefalea en trueno, FAST positivo, pérdida de consciencia, convulsión activa, fiebre + rigidez de nuca, pensamiento suicida | flag_alarma=TRUE → WhatsApp a neuroasesor interno con: nombre, teléfono, síntoma exacto, fase, guia_soporte | Informar que va a recibir atención especializada. En casos urgentes: indicar ir a urgencias. |
| Duda clínica | IA no puede clasificar con certeza el caso según las guías disponibles | fase_siguiente=HUMANO en respuesta JSON | Informar que un especialista de ICN lo contactará pronto. |
| Solicitud del paciente | Paciente pide explícitamente hablar con una persona | fase_siguiente=HUMANO | Confirmar que se conecta con el equipo ICN. |
| EPS detectada | Paciente menciona ser usuario de EPS | fase_siguiente=ADMIN → link icnsalud.com/#contacto | Redirigir al canal correcto con el link. |
| Resultado postconsulta — externo | En F5, paciente tiene órdenes o exámenes de fuera de ICN | fase_siguiente=HUMANO para gestión por asesor | Informar que un asesor lo apoyará con los próximos pasos. |

13. Puntos Críticos y Riesgos de Producción

| Riesgo | Descripción | Mitigación |
| --- | --- | --- |
| JSON inválido de ChatGPT | Si la IA genera texto libre en lugar de JSON, Make falla al parsear. | Módulo de validación JSON en Make. Si falla: retry con prompt de corrección. Máx 2 reintentos. Si persiste: escalamiento a HUMANO. |
| Lenguaje de diagnóstico | ChatGPT puede usar frases como 'Tienes X' si el prompt no es suficientemente estricto. | El prompt base incluye regla explícita y ejemplos de lenguaje prohibido. Auditoría aleatoria de conversaciones cada semana. |
| Historial JSON largo | Conversaciones largas elevan costo y pueden exceder contexto de GPT-4o. | Máximo 20 turnos en historial_json. Truncar los más antiguos automáticamente. |
| Alarma clínica no detectada | IA puede pasar por alto bandera roja si el usuario la describe de forma indirecta. | Filtro adicional en Make ANTES de llamar a ChatGPT: búsqueda de keywords de alarma en el mensaje bruto. |
| Reporte visual no generado | Si el Escenario 2 falla, el paciente no recibe su reporte. | Reintentar automáticamente 2 veces. Si falla: notificar al equipo ICN para envío manual. Registrar en Sheets. |
| Omisión de F3 | Agente salta F3 si el prompt de F2 no está bien configurado. | F2 siempre debe tener fase_siguiente=F3. Validar en Make antes de ejecutar ChatGPT. |
| Acceso no autorizado a Sheets | Google Sheets con datos de salud expuestos. | Solo cuentas @icnsalud.com con 2FA. Make accede con cuenta de servicio de permisos mínimos. Auditoría mensual. |
| Costos API crecientes | Alto volumen puede elevar costos de GPT-4o. | Monitorear tokens/mes. Si supera presupuesto: F5 y F6 con mensajes estáticos, IA solo en F1–F4. |
| Paciente existente en nuevo número | Si paciente cambia de número, se crea registro duplicado. | V1: aceptar como limitación. V2: identificación por nombre + fecha de nacimiento como clave adicional. |



---

# FUENTE V2: NeuroOrientador V2 (1).docx

**Rol de esta fuente:** Base legal/metodológica y arquitectura inicial ampliada.


NeurOrientador

ICN Salud — Sistema Clínico de Teleorientación Neurológica

Documentación Técnica de Implementación — Versión 2.0

Stack: WhatsApp Business API  ·  Make  ·  ChatGPT API  ·  Google Sheets

Base metodológica: ICHD-3 · DSM-5-TR · Guías ICN · Modelo UNI de Evaluación de Riesgo en Salud

2026

| Canal WhatsApp Business API | Automatización Make | IA ChatGPT API (GPT-4o) | Datos Google Sheets |
| --- | --- | --- | --- |

0. Declaración de Naturaleza del Servicio (Obligatorio legal)

| AVISO LEGAL — Debe aparecer en todos los puntos de contacto del sistema |
| --- |
| NeurOrientador es un sistema de TELEORIENTACIÓN EN SALUD NEUROLÓGICA. |
| No es una consulta médica. No emite diagnósticos clínicos. NO formula medicamentos. |
|  |
| El resultado de la evaluación es una CLASIFICACIÓN DE RIESGO EN SALUD, |
| basada en criterios clínicos validados (ICHD-3, DSM-5-TR, Guías ICN). |
|  |
| "Esto sugiere un nivel de riesgo... El especialista neurólogo podrá confirmar" |
|  |
| Este servicio está respaldado por ICN Salud y opera bajo el marco legal |
| de la Resolución 2654 de 2019 del Ministerio de Salud de Colombia. |

0.1 Lenguaje obligatorio del sistema

| Contexto | Lenguaje PROHIBIDO | Lenguaje OBLIGATORIO |
| --- | --- | --- |
| Resultado de evaluación | Tienes migraña / Eso es epilepsia | Esto sugiere un nivel de riesgo neurológico que amerita evaluación especializada |
| Clasificación de riesgo | Tu diagnóstico es... | El resultado de tu teleorientación indica... |
| Recomendación | Debes tomar este medicamento | El especialista podrá confirmar y definir el manejo más adecuado |
| Presentación del agente | Soy tu médico virtual | Soy NeurOrientador, el asistente de teleorientación de ICN Salud |
| Cierre de evaluación | Ya sabemos qué tienes | Tu evaluación de riesgo está completa. Este resultado no es un diagnóstico médico |

0.2 Separación legal: teleorientación vs. telemedicina

| Servicio | Fases del agente | Qué hace | Qué NO hace | Marco legal |
| --- | --- | --- | --- | --- |
| Teleorientación (este sistema) | F0 → F4 | Clasifica riesgo, orienta, recomienda consulta | Diagnosticar, formular, tratar | Res. 2654/2019 — Teleorientación |
| Consulta médica / Telemedicina | Fuera del agente | Diagnóstico, formulación, seguimiento clínico | No aplica aquí | Res. 2654/2019 — Telemedicina |

1. Base Clínica y Metodológica

Todo el flujo clínico de NeurOrientador está fundamentado en guías de manejo validadas internacionalmente y adoptadas por ICN Salud. Cada decisión del árbol conversacional tiene trazabilidad directa a un criterio clínico documentado.

1.1 Marco metodológico principal — Modelo UNI de Evaluación de Riesgo en Salud

| Modelo UNI — Fundamento del sistema de puntuación y clasificación |
| --- |
| Todo el flujo de NeurOrientador parte del Modelo de Evaluación de Riesgo en Salud UNI, |
| desarrollado por ICN Salud. Este modelo define: |
|  |
| • La lógica de puntuación por dominios (D1–D6) |
| • Los umbrales de clasificación: Bajo / Moderado / Alto / Alarma |
| • Las rutas de salida según el nivel de riesgo calculado |
| • Los fenotipos clínicos probables por programa |
|  |
| El sistema de scoring de F3 implementa directamente este modelo, |
| asignando pesos a cada respuesta según los criterios UNI validados por el equipo médico ICN. |

1.2 Guías clínicas por programa y correspondencia CIE-10

| Programa | Guía base | Versión | Criterios aplicados en F3 | Clasificación CIE-10 de salida |
| --- | --- | --- | --- | --- |
| Cefalea / Migraña | ICHD-3 (International Headache Classification) | 3ra edición, 2018 | Criterios A–E para migraña con/sin aura, tipo, frecuencia, severidad, respuesta a analgésicos | G43.x (Migraña), G44.x (Otras cefaleas) |
| Neurodesarrollo | DSM-5-TR (APA) Escala de TDAH ICN | 2022 | Criterios de TDAH (Criterio A–E), TEA (Criterios A–B), retraso del desarrollo | F84.x (TEA), F90.x (TDAH), F88 (Retraso) |
| Epilepsia | Guía ILAE 2017 + Guía MPS Colombia | 2017 / actualizada | Tipo de crisis, frecuencia, adherencia, triggers, impacto funcional | G40.x (Epilepsia) |
| Trastornos del sueño | ICSD-3 (American Academy of Sleep Medicine) | 3ra edición | Insomnio, higiene del sueño, somnolencia, apnea sospechada | G47.x (Trastornos del sueño) |
| Memoria / Deterioro cognitivo | Guías NIA-AA + Guías ICN | 2018 / ICN | MMSE adaptado conversacional, inicio, progresión, impacto en ABVD | F06.7 (DCL), G30.x (Alzheimer), F03 (Demencia NE) |
| ACV | Guía AHA/ASA + Guías ICN | 2021 / ICN | FAST adaptado, factores de riesgo, tiempo de inicio — protocolo alarma estricta | I63.x (Infarto cerebral), I60.x (Hemorragia) |
| Parálisis facial | Guía práctica EAN | 2019 | Grado House-Brackmann adaptado, tiempo de inicio, compromiso ocular | G51.0 (Parálisis de Bell) |
| Movimiento / Parkinson | Guías MDS | 2020 | Escala MDS-UPDRS adaptada conversacional, tipo de temblor, rigidez, bradicinesia | G20 (Parkinson), G25.x (Otros mov.) |
| Dolor neuropático | Guías IASP + NeuPSIG | 2019 | DN4 adaptado conversacional, distribución, características, comorbilidades | G62.x (Neuropatía) |
| Neuromuscular | Guías AANEM + ICN | ICN | Debilidad, distribución, progresión, compromiso respiratorio | G70.x (Unión NM), G71.x (Miopatía) |

1.3 Trazabilidad clínica — Campo obligatorio en cada decisión

Cada decisión de clasificación del sistema debe registrar qué guía soporta la decisión. Este campo es obligatorio en el dashboard interno de F3 y en la hoja Google Sheets.

| Ejemplo de campo guia_soporte en respuesta JSON de ChatGPT (F3) |
| --- |
| { |
| "respuesta_visible": "Con base en lo que me contaste...", |
| "fase_siguiente": "F4", |
| "campos_actualizar": { |
| "nivel_riesgo": "Alto", |
| "fenotipo_probable": "Migraña episódica de alta frecuencia" |
| }, |
| "guia_soporte": "ICHD-3 — Criterios A-E migraña sin aura (G43.009)", |
| "cie10": "G43.009", |
| "flag_alarma": false, |
| "notas_internas": "Score 13/15. Criterio ICHD-3 cumplido: ≥5 episodios, 4-72h, pulsátil unilateral, intensidad moderada-severa, náuseas, fotofobia." |
| } |

2. Arquitectura Técnica del Sistema

NeurOrientador integra tres capas tecnológicas orquestadas por Make. El canal de entrada es WhatsApp Business API, la inteligencia está en ChatGPT (GPT-4o) y la persistencia de datos opera en Google Sheets.

2.1 Diagrama de flujo de datos

| Flujo de datos — Arquitectura completa |
| --- |
| USUARIO (WhatsApp) |
| ↓  mensaje entrante |
| WHATSAPP BUSINESS API → webhook HTTP POST → Make |
| ↓ |
| MAKE — Escenario 1 (conversación principal) |
| ├─ Buscar paciente en Google Sheets (por teléfono) |
| ├─ Recuperar historial_json + fase_actual + datos clínicos |
| ├─ Seleccionar system prompt según fase_actual |
| ├─ Llamar ChatGPT API (GPT-4o) con contexto completo |
| ├─ Parsear respuesta JSON estructurada |
| ├─ Actualizar Google Sheets (paciente + conversaciones + citas) |
| ├─ Si flag_alarma = TRUE → notificar humano |
| └─ Enviar respuesta_visible al paciente por WhatsApp |
| ↓  (si aplica) |
| MAKE — Escenario 2: generar imagen reporte visual → enviar por WhatsApp |
| ↓  (programado) |
| MAKE — Escenario 3: recordatorios F5 (diario 8am) |
| MAKE — Escenario 4: seguimiento preventivo F6 (lunes, miércoles, viernes 9am) |

2.2 Stack tecnológico

| Componente | Herramienta | Rol | Consideraciones clave |
| --- | --- | --- | --- |
| Canal | WhatsApp Business API (Meta Cloud API) | Recibir y enviar mensajes | Número verificado en Meta Business Manager. Webhook activo 24/7 |
| Orquestador | Make — plan Core o superior | Conectar todos los módulos, gestionar flujo, enrutar fases | Escenario principal activo permanentemente. Alertas de error configuradas |
| Inteligencia artificial | ChatGPT API — GPT-4o | Procesar mensajes, aplicar lógica de fase, generar respuestas JSON | Historial completo enviado en cada llamada. Respuesta siempre en JSON estructurado |
| Base de datos | Google Sheets | Pacientes, conversaciones, citas, cohortes de investigación | Control de acceso estricto. Solo cuentas ICN autorizadas. 4 hojas operativas |
| Generación de reporte visual | Make + servicio de imagen (API imgbb o similar) | Generar imagen del reporte de riesgo al cierre de F3/F4 | Imagen enviada por WhatsApp. Incluye disclaimer legal obligatorio |
| Agenda particulares | Google Calendar o Calendly API (vía Make) | Consultar disponibilidad y agendar en F4 | Bloques específicos para particulares definidos con Jeneth. Redirección a web como alternativa |
| Notificación humano | WhatsApp número interno ICN / Email | Alertar a neuroasesor en casos de alarma o solicitud | Mensaje estructurado con: nombre, teléfono, síntoma, resumen clínico |

3. Consentimiento Informado — F1 (Obligatorio legal)

El consentimiento informado es el primer paso obligatorio de F1 antes de capturar cualquier dato del paciente. Debe cubrir cuatro elementos legales, quedar registrado en Google Sheets y usar lenguaje claro y accesible.

3.1 Componentes obligatorios del consentimiento

| Componente | Contenido obligatorio | Base legal | Registro en Sheets |
| --- | --- | --- | --- |
| Tratamiento de datos | Informar que los datos personales y de salud serán tratados con confidencialidad. Indicar finalidad: orientación clínica, investigación anonimizada ICN, seguimiento. | Ley 1581 de 2012 — Habeas Data. Decreto 1377 de 2013. | Campo: consentimiento_datos = TRUE/FALSE + timestamp |
| Naturaleza del servicio | Explicar que esto es una teleorientación en salud neurológica, no una consulta médica. El resultado es una clasificación de riesgo, no un diagnóstico. | Res. 2654/2019 — Teleorientación en salud | Campo: consentimiento_servicio = TRUE/FALSE |
| Alcance del sistema | Informar que el agente NO diagnostica, NO formula medicamentos y NO reemplaza al especialista. | Ley 23 de 1981 — Ética médica | Incluido en consentimiento_servicio |
| Uso en investigación | Informar que los datos anonimizados podrán ser usados para investigación clínica ICN e identificación de patrones poblacionales. | Res. 8430 de 1993 — Investigación en salud | Campo: consentimiento_investigacion = TRUE/FALSE |

3.2 Texto exacto del consentimiento (mensaje F1)

| MENSAJE DE CONSENTIMIENTO — Enviar al inicio de F1 Hola, bienvenido/a a ICN Salud. Soy NeurOrientador, el sistema de teleorientación neurológica de ICN Salud. Antes de comenzar, necesito informarte tres cosas importantes: 1. PROTECCIÓN DE DATOS: Tu información personal y de salud será tratada con confidencialidad según la Ley 1581 de 2012. Tus datos se usarán solo para orientarte y, de forma anonimizada, para mejorar nuestros protocolos clínicos. 2. NATURALEZA DEL SERVICIO: Este es un servicio de TELEORIENTACIÓN en salud neurológica. El resultado que obtendrás es una evaluación de riesgo, NO un diagnóstico médico. No reemplaza la consulta con un especialista neurólogo. 3. LO QUE HACE EL SISTEMA: Evalúa tu nivel de riesgo neurológico y te orienta sobre el paso más adecuado. No puede diagnosticar ni formular medicamentos. ¿Aceptas estos términos y autorizas el tratamiento de tus datos para continuar con tu teleorientación? Responde SÍ o NO. |
| --- |

| Registro obligatorio en Google Sheets al recibir SÍ |
| --- |
| consentimiento_datos        = TRUE |
| consentimiento_servicio     = TRUE |
| consentimiento_investigacion = TRUE  (incluido en el SI general) |
| timestamp_consentimiento    = 2026-03-20T10:30:00 |
| ip_o_canal                  = WhatsApp |
|  |
| Si el usuario responde NO: el agente informa que sin autorización no puede |
| continuar, ofrece el canal web https://icnsalud.com/#contacto y cierra la sesión. |

4. Esquema de Datos — Google Sheets

El sistema opera con cuatro hojas en un mismo Google Sheets. El acceso está restringido exclusivamente a cuentas institucionales de ICN Salud con autenticación de dos factores.

| Control de acceso obligatorio — Google Sheets |
| --- |
| • Solo cuentas @icnsalud.com con acceso explícito pueden ver o editar el Sheets |
| • Make accede mediante cuenta de servicio con permisos mínimos necesarios |
| • Auditoría de acceso activa (Google Workspace Admin) |
| • Sin acceso público, sin links compartidos abiertos |
| • Política de retención: datos eliminados o anonimizados a los 5 años |

4.1 Hoja 1: PACIENTES

Una fila por paciente. Clave primaria: número de teléfono WhatsApp. Se crea en F1 y se actualiza en cada fase.

| Campo | Tipo | Descripción | Ejemplo |
| --- | --- | --- | --- |
| paciente_id | Texto (auto) | ID único generado por Make | PAC-20260320-001 |
| telefono | Texto | Número WhatsApp — clave primaria | 573041234567 |
| nombre | Texto | Nombre capturado en F1 | María Torres |
| edad | Número | Edad en años | 38 |
| ciudad | Texto | Ciudad de residencia | Medellín |
| aseguramiento | Texto | Particular / Prepagada (EPS → icnsalud.com/#contacto) | Prepagada |
| entidad_prepagada | Texto | Nombre de la prepagada si aplica | Sura |
| consentimiento_datos | Booleano | TRUE si autorizó tratamiento de datos en F1 | TRUE |
| consentimiento_servicio | Booleano | TRUE si aceptó términos de teleorientación | TRUE |
| consentimiento_investigacion | Booleano | TRUE si autorizó uso en investigación ICN | TRUE |
| timestamp_consentimiento | Fecha-hora | Momento exacto de aceptación del consentimiento | 2026-03-20T10:30:00 |
| fase_actual | Texto | Fase activa del agente (F0 a F6) | F4 |
| programa_clinico | Texto | Programa neurológico asignado | Cefalea |
| guia_soporte | Texto | Guía clínica que soporta la clasificación actual | ICHD-3 — Migraña sin aura G43.009 |
| cie10 | Texto | Código CIE-10 del fenotipo probable | G43.009 |
| nivel_riesgo | Texto | Bajo / Moderado / Alto / Alarma | Alto |
| score_total | Número | Puntaje acumulado del scoring F3 | 13 |
| fenotipo_probable | Texto | Fenotipo clínico probable (sin diagnóstico definitivo) | Migraña episódica de alta frecuencia |
| respuestas_orientacion | JSON (Texto) | Respuestas del paciente a los 6 dominios D1–D6 stringificadas | {"D1":"pulsatil","D2":"nauseas",...} |
| reporte_enviado | Booleano | TRUE si ya se envió la imagen del reporte visual | FALSE |
| conversion | Texto | Tipo de conversión lograda en F4 | Paquete diagnóstico cefalea |
| fecha_cita | Fecha | Fecha de cita agendada | 2026-03-26 |
| canal_agenda | Texto | Directo (agente) / Web (redirección) | Directo |
| estado_cita | Texto | Pendiente / Confirmada / Asistió / No asistió | Confirmada |
| fecha_primera_orientacion | Fecha | Fecha de la primera teleorientación completada | 2026-03-20 |
| fecha_ultima_orientacion | Fecha | Fecha de la última teleorientación (control cada 6 meses) | 2026-03-20 |
| cohorte | Texto | Clasificación para investigación: programa+riesgo+fenotipo | Cefalea_Alto_MigrañaFrecuente |
| requiere_humano | Booleano | TRUE si se activó escalamiento a asesor | FALSE |
| fecha_creacion | Fecha-hora | Timestamp de primer contacto | 2026-03-20T10:30:00 |
| ultima_actividad | Fecha-hora | Timestamp del último mensaje recibido | 2026-03-20T11:15:00 |
| historial_json | JSON (Texto) | Array de mensajes para contexto de ChatGPT (últimos 20 turnos) | [{role:user,...},{role:assistant,...}] |
| notas_internas | Texto | Campo libre para equipo clínico ICN | Historial familiar migraña |

4.2 Hoja 2: CONVERSACIONES

Una fila por turno. Permite auditoría completa de cada interacción y trazabilidad de decisiones clínicas.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| conv_id | Texto (auto) | ID único del turno: CONV-{paciente_id}-{timestamp} |
| paciente_id | Texto | Referencia al paciente (FK → PACIENTES) |
| telefono | Texto | Número WhatsApp (lookup rápido) |
| fase | Texto | Fase activa en ese turno (F0–F6) |
| mensaje_usuario | Texto | Mensaje exacto enviado por el paciente |
| respuesta_agente | Texto | Respuesta generada por ChatGPT y enviada al paciente |
| guia_soporte_turno | Texto | Guía clínica que soportó la decisión en ese turno específico |
| timestamp | Fecha-hora | Fecha y hora exacta del turno |
| tokens_usados | Número | Tokens consumidos en la llamada a la API de ChatGPT |
| flag_alarma | Booleano | TRUE si el turno activó una bandera roja clínica |
| escalado_humano | Booleano | TRUE si en ese turno se notificó al neuroasesor |

4.3 Hoja 3: CITAS

Una fila por cita o paquete convertido. Alimenta el seguimiento en F5.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| cita_id | Texto (auto) | ID único de la cita: CITA-{paciente_id}-{fecha} |
| paciente_id | Texto | FK → PACIENTES |
| tipo | Texto | Consulta / Paquete diagnóstico / Tratamiento |
| programa | Texto | Programa clínico asociado |
| fecha_cita | Fecha | Fecha programada |
| hora_cita | Texto | Hora programada |
| canal_agenda | Texto | Directo (agente) / Web — según ruta tomada en F4 |
| recordatorio_3d | Booleano | TRUE si ya se envió recordatorio -3 días |
| recordatorio_1d | Booleano | TRUE si ya se envió recordatorio -1 día |
| confirmacion | Texto | Pendiente / Confirmada / Cancelada |
| seguimiento_post | Booleano | TRUE si ya se realizó el seguimiento postconsulta |
| resultado_post | Texto | Medicamentos / Terapias / Exámenes ICN / Exámenes externos / Sin novedad |

4.4 Hoja 4: COHORTES_INVESTIGACION

Hoja de solo lectura para el equipo de investigación. Se alimenta automáticamente desde PACIENTES cuando se completa F3. Datos anonimizados para análisis clínico y publicaciones ICN.

| Campo | Descripción |
| --- | --- |
| cohorte_id | ID único de la entrada en investigación |
| programa_clinico | Programa neurológico evaluado |
| guia_soporte | Guía clínica base de la clasificación |
| cie10 | Código CIE-10 del fenotipo probable |
| nivel_riesgo | Bajo / Moderado / Alto / Alarma |
| fenotipo_probable | Fenotipo clínico identificado |
| score_total | Puntaje numérico total |
| respuestas_orientacion | JSON con respuestas D1–D6 (sin datos personales) |
| edad | Edad del paciente (anonimizado) |
| ciudad | Ciudad (anonimizado, solo para epidemiología) |
| fecha_evaluacion | Fecha de la teleorientación |
| conversion | ¿Se convirtió a consulta/paquete? Sí/No |
| fecha_cita | Fecha de cita si aplica (anonimizado) |

5. Flujos de Make — Escenarios de Automatización

El sistema opera con cuatro escenarios en Make. Cada uno tiene un propósito específico y se activa por un trigger diferente.

5.1 Escenario 1: Conversación principal (webhook permanente)

| Trigger: Webhook HTTP ← WhatsApp Business API |
| --- |
| Activo 24/7. Se dispara cada vez que el paciente envía un mensaje. |

| 1 | [Webhook]  Recibir mensaje de WhatsApp Parsear: numero_telefono, mensaje_texto, timestamp. Verificar firma HMAC del webhook. |
| --- | --- |

| 2 | [Google Sheets — Buscar fila]  Buscar paciente por teléfono Filtro: columna telefono = numero_recibido. Si no existe → paso 3a. Si existe → paso 3b. |
| --- | --- |

| 3a | [Google Sheets — Crear fila]  Crear nuevo paciente Insertar en PACIENTES: telefono, fecha_creacion, fase_actual=F0, historial_json=[], consentimientos=FALSE. |
| --- | --- |

| 3b | [Google Sheets — Leer fila]  Recuperar datos del paciente Obtener: fase_actual, historial_json, programa_clinico, nivel_riesgo, nombre, consentimientos, guia_soporte. |
| --- | --- |

| 4 | [Herramienta — JSON Parse]  Deserializar historial Convertir historial_json (string) a array de objetos para enviar a ChatGPT. |
| --- | --- |

| 5 | [Router — Switch]  Seleccionar system prompt por fase Según fase_actual: F0, F1, F2, F3, F4, F5, F6, ADMIN, HUMANO → cargar el prompt correspondiente. |
| --- | --- |

| 6 | [ChatGPT — Create Completion]  Llamar a GPT-4o Model: gpt-4o \| Max tokens: 800 \| Messages: [system_prompt_fase + historial + mensaje_actual]. |
| --- | --- |

| 7 | [Herramienta — JSON Parse]  Parsear respuesta JSON de IA Extraer: respuesta_visible, fase_siguiente, campos_actualizar, guia_soporte, cie10, flag_alarma, notas_internas. |
| --- | --- |

| 8 | [Google Sheets — Actualizar PACIENTES]  Actualizar datos del paciente Escribir todos los campos_actualizar + fase_actual, guia_soporte, cie10, ultima_actividad, requiere_humano. |
| --- | --- |

| 9 | [Google Sheets — Crear fila CONVERSACIONES]  Registrar turno Insertar: conv_id, paciente_id, fase, mensaje_usuario, respuesta_agente, guia_soporte_turno, timestamp, tokens, flag_alarma. |
| --- | --- |

| 10 | [Herramienta — Array + JSON]  Actualizar historial JSON Agregar turno actual al array. Si >20 turnos, eliminar el más antiguo. Stringificar. |
| --- | --- |

| 11 | [Google Sheets — Actualizar PACIENTES]  Persistir historial actualizado Escribir nuevo historial_json en campo del paciente. |
| --- | --- |

| 12 | [Router — Condicional]  Verificar fase_siguiente = ADMIN Si ADMIN → enviar mensaje con link https://icnsalud.com/#contacto y cerrar flujo. |
| --- | --- |

| 13 | [Router — Condicional]  Verificar flag_alarma Si flag_alarma = TRUE → paso 14. Si FALSE → paso 15. |
| --- | --- |

| 14 | [WhatsApp — Enviar mensaje (neuroasesor)]  Notificar escalamiento humano Enviar al número interno ICN: nombre, teléfono, síntoma de alarma, guia_soporte, resumen clínico. |
| --- | --- |

| 15 | [Router — Condicional]  Verificar si F3 completada Si fase_siguiente es F4 o F6 y reporte_enviado=FALSE → paso 16. Si no → paso 17. |
| --- | --- |

| 16 | [Escenario 2 (sub-call)]  Generar y enviar reporte visual Llamar Escenario 2 para generar imagen del reporte de riesgo y enviarla al paciente. |
| --- | --- |

| 17 | [WhatsApp — Enviar mensaje (paciente)]  Enviar respuesta al paciente Enviar respuesta_visible al número WhatsApp del paciente. |
| --- | --- |

5.2 Escenario 2: Reporte visual de riesgo

| Trigger: Llamada desde Escenario 1 (al completar F3 o F4) |
| --- |
| Genera automáticamente la imagen del reporte de riesgo y la envía por WhatsApp. |
| Incluye obligatoriamente el disclaimer legal de teleorientación. |

| 1 | [Recibir datos]  Recibir parámetros del Escenario 1 Nombre, nivel_riesgo, fenotipo_probable, programa_clinico, guia_soporte, recomendacion, cie10. |
| --- | --- |

| 2 | [Herramienta — Text Formatter]  Construir contenido del reporte Armar el texto del reporte: encabezado ICN, nombre paciente, programa, nivel de riesgo (con colores), fenotipo probable, recomendación, disclaimer legal. |
| --- | --- |

| 3 | [HTTP — POST (API de imagen)]  Generar imagen del reporte Llamar a servicio de generación de imagen (Bannerbear, imgbb, o HTML-to-image API). Pasar HTML/JSON con branding ICN. |
| --- | --- |

| 4 | [WhatsApp — Enviar imagen]  Enviar reporte visual al paciente Enviar la imagen generada con caption: 'Tu evaluación de riesgo neurológico de ICN Salud.' |
| --- | --- |

| 5 | [Google Sheets — Actualizar PACIENTES]  Marcar reporte enviado Actualizar reporte_enviado = TRUE y timestamp_reporte en hoja PACIENTES. |
| --- | --- |

| 6 | [Google Sheets — Crear fila COHORTES]  Registrar en investigación Insertar fila anonimizada en COHORTES_INVESTIGACION con todos los campos clínicos. |
| --- | --- |

5.3 Escenario 3: Recordatorios y seguimiento F5 (diario)

| Trigger: Schedule → diariamente a las 8:00 AM (UTC-5, Colombia) |
| --- |
| Revisa CITAS y envía recordatorios o seguimientos según fecha y estado. |

| 1 | [Schedule]  Trigger diario 8:00 AM Ejecutar todos los días en zona horaria Colombia (UTC-5). |
| --- | --- |

| 2 | [Google Sheets — Buscar filas]  Citas en ventana ±3 días Filtrar hoja CITAS: fecha_cita entre hoy-1 y hoy+3, estado != Asistió. |
| --- | --- |

| 3 | [Iterator]  Iterar sobre citas Procesar cada cita individualmente. |
| --- | --- |

| 4 | [Router — Condicional fecha]  Determinar tipo de acción fecha=hoy+3 y rec_3d=FALSE → recordatorio -3d. fecha=mañana y rec_1d=FALSE → confirmación. fecha=ayer y seguimiento_post=FALSE → postconsulta. |
| --- | --- |

| 5a | [WhatsApp — Enviar mensaje]  Recordatorio -3 días Mensaje con nombre, fecha/hora, programa, instrucciones de preparación y dirección/modalidad. |
| --- | --- |

| 5b | [WhatsApp — Enviar mensaje]  Confirmación -1 día Pedir SÍ o NO. Si NO → ofrecer reprogramar. Si SÍ → actualizar estado_cita=Confirmada. |
| --- | --- |

| 5c | [ChatGPT + WhatsApp]  Seguimiento postconsulta Generar con IA mensaje de seguimiento personalizado. Preguntar resultado, órdenes, siguiente paso. |
| --- | --- |

| 6 | [Google Sheets — Actualizar CITAS]  Marcar acción ejecutada Actualizar recordatorio_3d, recordatorio_1d o seguimiento_post según el caso. |
| --- | --- |

5.4 Escenario 4: Seguimiento preventivo F6 (lunes, miércoles, viernes)

| Trigger: Schedule → lunes, miércoles y viernes a las 9:00 AM |
| --- |
| Gestiona el programa educativo de Fase 6 para pacientes activos en esa fase. |

| 1 | [Schedule]  Trigger 3 veces/semana Lunes, miércoles y viernes a las 09:00 AM hora Colombia. |
| --- | --- |

| 2 | [Google Sheets — Buscar filas]  Pacientes en Fase 6 Filtrar PACIENTES: fase_actual = F6. |
| --- | --- |

| 3 | [Iterator]  Iterar por paciente Procesar individualmente. |
| --- | --- |

| 4 | [ChatGPT — Create Completion]  Generar tríada educativa personalizada Prompt F6 + programa + riesgo + historial. Generar: 1 educación breve, 1 acción concreta, 1 pregunta de seguimiento. |
| --- | --- |

| 5 | [WhatsApp — Enviar mensaje]  Enviar tríada al paciente Mensaje claro, sin tecnicismos, en tono amigable. |
| --- | --- |

| 6 | [Google Sheets — Actualizar PACIENTES]  Registrar envío Actualizar ultima_actividad. |
| --- | --- |

6. Flujo por Fases — Reglas de Operación

| Regla operativa fundamental (no negociable) |
| --- |
| El agente debe ofrecer SIEMPRE la teleorientación (F3) a TODOS los pacientes |
| una vez completada F1, sin excepción. |
|  |
| No puede saltarse F3 aunque el paciente llegue preguntando por precio o cita. |
| Esto garantiza: entrada clínica estandarizada, calidad del dato, |
| fortalecimiento de la investigación y conversión basada en riesgo real. |
|  |
| Si el paciente ya realizó una teleorientación previamente: |
| → Sugerir repetirla cada 6 meses como control y actualización de riesgo. |
| (Comparar con fecha_ultima_orientacion en Google Sheets) |

| Fase | Nombre | Objetivo | Entrada mínima | Salida | Condición de transición | Teleorientación o Telemedicina |
| --- | --- | --- | --- | --- | --- | --- |
| F0 | Clasificación | Detectar intención | Mensaje libre | tipo_contacto | Siempre → F1 o ADMIN | Teleorientación |
| F1 | Identificación | Consentimiento + datos básicos | Mensaje entrante nuevo | perfil_básico completo + consentimientos = TRUE | Datos + consentimiento OK → F2 | Teleorientación |
| F2 | Necesidad | Confirmar que pasa por F3 | perfil_básico | motivo_orientacion confirmado | Siempre → F3 (ver regla fundamental) | Teleorientación |
| F3 | Teleorientación | Árbol clínico + scoring + reporte | motivo + datos básicos | nivel_riesgo + fenotipo + reporte visual enviado | Bajo → F6 \| Mod/Alto → F4 \| Alarma → HUMANO | Teleorientación |
| F4 | Conversión | Agenda + paquete diagnóstico | Riesgo + programa + agenda disponible | conversión o escalado | Acepta → F5 \| Rechaza → F6 \| Humano → HUMANO | Teleorientación (orientación comercial) |
| F5 | Seguimiento | Recordatorios + postconsulta | Cita convertida + fecha | asistencia + resultado_post | Postconsulta clasificada → F6 o F4 | Teleorientación |
| F6 | Prevención | Educación + remarketing + investigación | nivel_riesgo + programa | adherencia + señales de reactivación | Síntoma nuevo → F3 \| Interés → F4 \| Alarma → HUMANO | Teleorientación |
| ADMIN | Administrativo | Redirigir a canal correcto | Solicitud admin / EPS | Link icnsalud.com/#contacto | Fin de conversación en agente | Fuera del agente |
| HUMANO | Escalamiento | Transferir a neuroasesor | Alarma / solicitud / duda | Notificación a equipo ICN | Fin de conversación en agente | Puede ser Telemedicina — servicio independiente |

7. Integración de Agenda — Pacientes Particulares (F4)

Acordado con Jeneth: se habilitarán bloques específicos de agenda para pacientes particulares. El agente puede agendar directamente o redirigir a la web según la disponibilidad.

7.1 Flujo de agenda en F4

| Lógica de agenda en Fase 4 |
| --- |
| Cuando el paciente acepta agendar en F4: |
|  |
| 1. Make consulta disponibilidad en Google Calendar / Calendly (API) |
| Filtro: bloques habilitados para particulares |
|  |
| 2. Si hay disponibilidad en las próximas 72h: |
| → El agente ofrece 2-3 opciones de horario directamente en el chat |
| → El paciente elige y Make confirma la cita automáticamente |
| → Se crea fila en hoja CITAS con canal_agenda = 'Directo' |
|  |
| 3. Si NO hay disponibilidad inmediata o el sistema no puede confirmar: |
| → El agente redirige: 'Puedes agendar directamente en icnsalud.com' |
| → Se registra canal_agenda = 'Web' en CITAS |
|  |
| 4. En ambos casos: Make crea fila en CITAS y activa el Escenario 3 (F5). |

7.2 Requisitos técnicos de la integración

| Componente | Configuración necesaria | Responsable |
| --- | --- | --- |
| Google Calendar o Calendly | Crear calendario específico para particulares. Definir bloques disponibles con Jeneth. Conectar API en Make. | ICN (Jeneth) + Técnico |
| Make — módulo Calendar | Módulo 'List Events' o 'Create Event' de Google Calendar / Calendly. Filtrar por tipo de paciente = Particular. | Técnico Make |
| Manejo de conflictos | Si el slot se toma entre que el agente lo ofrece y el paciente confirma: ofrecer alternativa automáticamente. | Técnico Make |
| Notificación al equipo | Cuando se confirma cita directa: Make envía notificación al equipo ICN (WhatsApp o email). | Técnico Make |

8. Prompts de ChatGPT por Fase

Todos los prompts usan el formato JSON estructurado para que Make procese las respuestas automáticamente. El lenguaje de teleorientación es obligatorio en todos.

| Formato JSON obligatorio de respuesta — Todas las fases |
| --- |
| { |
| "respuesta_visible": "Texto que se enviará al paciente por WhatsApp", |
| "fase_siguiente": "F0\|F1\|F2\|F3\|F4\|F5\|F6\|ADMIN\|HUMANO", |
| "campos_actualizar": { }, |
| "guia_soporte": "ICHD-3 criterio X / DSM-5-TR criterio Y / Guía ICN", |
| "cie10": "G43.009", |
| "flag_alarma": false, |
| "notas_internas": "Texto solo visible para equipo clínico ICN" |
| } |
|  |
| guia_soporte y cie10 son obligatorios solo cuando se completa F3. |
| flag_alarma = true activa escalamiento inmediato a neuroasesor humano. |

8.1 Prompt base del sistema (incluir en todas las fases)

| SYSTEM PROMPT BASE Eres NeurOrientador, el sistema de teleorientación neurológica de ICN Salud. Tu rol es orientar a los pacientes mediante una evaluación estructurada de riesgo neurológico. Eres amable, empático y profesional. REGLAS ABSOLUTAS E INNEGOCIABLES: 1. Responde SIEMPRE en formato JSON válido (estructura definida). 2. NUNCA emitas diagnóstico definitivo. Lenguaje obligatorio: 'Esto sugiere un nivel de riesgo...' / 'El especialista podrá confirmar...' 3. NUNCA formules medicamentos ni recomiendes dosis. 4. SIEMPRE escala a HUMANO si detectas: pensamiento suicida, dolor torácico, pérdida de consciencia, convulsión activa, ACV probable (FAST positivo), cefalea en trueno, fiebre + rigidez de nuca. 5. SIEMPRE presenta el servicio como teleorientación, no como consulta médica. 6. Todos los pacientes deben pasar por F3 (teleorientación), sin excepción. Datos actuales del paciente: - Nombre: {{nombre}} \| Edad: {{edad}} \| Ciudad: {{ciudad}} - Aseguramiento: {{aseguramiento}} \| Fase: {{fase_actual}} - Programa: {{programa_clinico}} \| Riesgo previo: {{nivel_riesgo}} - Última orientación: {{fecha_ultima_orientacion}} |
| --- |

8.2 Prompt Fase 0 — Clasificación inicial

| PROMPT F0 {{SYSTEM_PROMPT_BASE}} FASE: F0 — Clasificar intención del primer mensaje. REGLAS: - Síntomas neurológicos / interés clínico / precio / cita → fase_siguiente: F1 - EPS / autorización / historia clínica / admin → fase_siguiente: ADMIN (En ADMIN: respuesta_visible debe incluir link https://icnsalud.com/#contacto) - Prepagada / particular → fase_siguiente: F1 En respuesta_visible: saludo breve ICN Salud. |
| --- |

8.3 Prompt Fase 1 — Consentimiento e identificación

| PROMPT F1 {{SYSTEM_PROMPT_BASE}} FASE: F1 — Consentimiento informado + datos básicos. PASO 1 — Si consentimiento_datos = FALSE: Enviar el mensaje completo de consentimiento (Ley 1581/2012, naturaleza del servicio, uso en investigación). Esperar SÍ o NO. Si NO: respuesta_visible con info de https://icnsalud.com/#contacto. Si SÍ: campos_actualizar = {consentimiento_datos:true, consentimiento_servicio:true, consentimiento_investigacion:true, timestamp_consentimiento: [ahora]} PASO 2 — Una vez consintió: capturar nombre, edad, ciudad, aseguramiento. Si EPS: respuesta_visible con link icnsalud.com/#contacto, fase_siguiente: ADMIN. Si Prepagada: solicitar nombre de la entidad y foto de orden si existe. MÁXIMO 2 preguntas por turno. NO hacer preguntas clínicas aquí. PASO 3 — Si nombre+edad+ciudad+aseguramiento completos: Mostrar brevemente los programas disponibles. Preguntar cuál describe mejor su situación. fase_siguiente: F2 Si paciente ya hizo orientación antes (fecha_ultima_orientacion no vacía y han pasado >6 meses): mencionar que se recomienda actualizar la evaluación. |
| --- |

8.4 Prompt Fase 2 — Confirmación de ruta

| PROMPT F2 {{SYSTEM_PROMPT_BASE}} FASE: F2 — Confirmar que el paciente pasará por F3. REGLA: Todos los pacientes deben pasar por F3 sin excepción. Si el paciente pide precio o cita directamente: explicar que primero se hace la evaluación de riesgo (teleorientación) para orientarlo mejor. En 1-2 turnos: confirmar el programa clínico e iniciar F3. fase_siguiente: F3 siempre. |
| --- |

8.5 Prompt Fase 3 — Teleorientación neurológica

| PROMPT F3 — NÚCLEO CLÍNICO (ejemplo: programa Cefalea / ICHD-3) {{SYSTEM_PROMPT_BASE}} FASE: F3 — Teleorientación neurológica estructurada. Programa: {{programa_clinico}} \| Score acumulado: {{score_total}} Guía base: ICHD-3 (Cefalea) \| Adaptar guía según programa activo. ÁRBOL CONVERSACIONAL — 6 DOMINIOS (1-2 preguntas por turno máximo): D1 CONFIRMACIÓN (mapea ICHD-3 Criterio B — características del dolor): '¿El dolor es pulsátil o en presión? ¿En qué zona?' Score: pulsátil unilateral +2 \| bilateral/presión +1 \| otro +0 D2 ALARMA (banderas rojas — escalar inmediatamente si presentes): '¿Ha tenido fiebre, vómito en proyectil, visión doble, pérdida de fuerza, el peor dolor de su vida de inicio súbito, rigidez en la nuca?' Score: ninguno +0 \| uno +1 \| DOS O MÁS → flag_alarma: true D3 CARACTERIZACIÓN (mapea ICHD-3 Criterio A — frecuencia y duración): '¿Cuántas veces por semana/mes? ¿Desde hace cuánto?' Score: <1/semana +1 \| 1-2/semana +2 \| ≥3/semana o crónico +3 D4 SEVERIDAD (mapea ICHD-3 Criterio C — intensidad y limitación): '¿Del 0 al 10 cuánto le afecta la vida diaria?' Score: 1-4 +1 \| 5-7 +2 \| 8-10 +3 D5 FENOTIPO (mapea ICHD-3 Criterio C — síntomas asociados): '¿Sensibilidad a luz, ruido, náuseas, aura visual?' Score: uno +1 \| dos +2 \| tres o más +3 D6 SALIDA (historial de tratamiento y comorbilidades): '¿Ha tomado medicamento? ¿Con qué resultado?' Score: sin medicamento/sin efecto +3 \| efecto parcial +2 \| buen control +1 CLASIFICACIÓN FINAL (score máximo 15): 0-4: Bajo → fase_siguiente: F6 5-8: Moderado → fase_siguiente: F4 9-12: Alto → fase_siguiente: F4 13-15 o flag_alarma=true: Alarma → fase_siguiente: HUMANO Al completar los 6 dominios, incluir en campos_actualizar: score_total, nivel_riesgo, fenotipo_probable, guia_soporte (ej: 'ICHD-3 G43.009 — Migraña episódica de alta frecuencia'), cie10, respuestas_orientacion (JSON con D1-D6), fecha_ultima_orientacion. En respuesta_visible usar lenguaje de teleorientación SIEMPRE: 'Esto sugiere un nivel de riesgo neurológico...' 'El especialista podrá confirmar...' NUNCA decir: 'Tienes X' / 'Tu diagnóstico es X'. |
| --- |

8.6 Prompt Fase 4 — Conversión clínica

| PROMPT F4 {{SYSTEM_PROMPT_BASE}} FASE: F4 — Conversión clínica y comercial. Riesgo: {{nivel_riesgo}} \| Fenotipo: {{fenotipo_probable}} \| CIE-10: {{cie10}} ESTRUCTURA DE CONVERSACIÓN F4: T1: Resumir hallazgos de la teleorientación con lenguaje prudente. Explicar por qué amerita evaluación especializada. T2: Presentar paquete diagnóstico del programa. Mencionar qué incluye. T3: Si hay objeción → manejarla (ver abajo). Si pregunta por agenda → consultar disponibilidad (Escenario 1 llama Google Calendar/Calendly). T4: Ofrecer 2-3 opciones de horario o redirigir a icnsalud.com si no hay. MANEJO DE OBJECIONES: 'Es caro' → costo de tratamiento tardío vs. valor del diagnóstico temprano 'Ya fui al médico' → valor del especialista neurólogo vs. médico general 'Tengo miedo' → validar, normalizar, enfocar en solución 'Quiero pensarlo' → respetar, ofrecer info adicional, acordar seguimiento 'Soy EPS' → redirigir a icnsalud.com/#contacto Si paciente pide humano → fase_siguiente: HUMANO Si acepta agenda directa → campos_actualizar={conversion:...,canal_agenda:'Directo'} Si se redirige a web → campos_actualizar={canal_agenda:'Web'} En ambos casos → fase_siguiente: F5 Si rechaza completamente → fase_siguiente: F6 |
| --- |

8.7 Prompt Fase 6 — Prevención, educación e investigación

| PROMPT F6 {{SYSTEM_PROMPT_BASE}} FASE: F6 — Seguimiento preventivo, educación y remarketing. Programa: {{programa_clinico}} \| Riesgo: {{nivel_riesgo}} Última orientación: {{fecha_ultima_orientacion}} Enviar la TRÍADA de seguimiento (máximo 4 líneas en total, lenguaje sencillo): 1. EDUCACIÓN: Un dato útil relacionado con el programa del paciente. 2. ACCIÓN: Una recomendación concreta que pueda hacer hoy. 3. PREGUNTA: Una pregunta simple de seguimiento de evolución. Contenido por programa: Cefalea: hidratación, sueño, manejo de estrés, diario de migraña Epilepsia: adherencia, sueño regular, evitar triggers, seguridad Sueño: higiene del sueño, horarios, cafeína, pantallas Memoria: estimulación cognitiva, actividad física, socialización ESCALAMIENTO DESDE F6: Síntomas empeoran → fase_siguiente: F3 Pregunta por consulta/paquete → fase_siguiente: F4 Angustia emocional intensa → fase_siguiente: HUMANO Han pasado ≥6 meses desde fecha_ultima_orientacion → sugerir actualizar la teleorientación, fase_siguiente: F3 |
| --- |

9. Simulación del Proceso Completo de Atención

Paciente: María Torres, 38 años, Medellín, Prepagada Sura. Motivo: dolores de cabeza frecuentes e intensos que le impiden trabajar.

|  | Turno 1  [F0 → F1] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Hola buenas, me han recomendado este número. Tengo unos dolores de cabeza muy fuertes que no me dejan trabajar. |  |
| Agente: |  | Hola, bienvenida a ICN Salud. Soy NeurOrientador, el sistema de teleorientación neurológica de ICN Salud. Con gusto te orientamos. Antes de comenzar necesito compartirte información importante sobre nuestro servicio. |  |
| Make: |  | Make crea fila nueva en PACIENTES: telefono=573041234567, fase_actual=F0. Escenario 1 paso 3a ejecutado. |  |
| Sheets: |  | PACIENTES: nueva fila creada. fase_actual=F0. consentimientos=FALSE. |  |
|  |  |  |  |

|  | Turno 2  [F1 — Consentimiento] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | [Paciente lee el mensaje] |  |
| Agente: |  | Antes de comenzar, te informo: (1) Tus datos se tratan con confidencialidad según la Ley 1581/2012. (2) Este es un servicio de TELEORIENTACIÓN, no una consulta médica — el resultado es una evaluación de riesgo, no un diagnóstico. (3) Tus datos anonimizados podrán usarse en investigación clínica ICN. ¿Aceptas estos términos? Responde SÍ o NO. |  |
| Make: |  | ChatGPT detecta paciente nuevo sin consentimiento. Genera mensaje de consentimiento completo. fase_actual=F1. |  |
| Sheets: |  | PACIENTES: fase_actual=F1. |  |
|  |  |  |  |

|  | Turno 3  [F1 — Datos básicos] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Sí, acepto. |  |
| Agente: |  | Perfecto, gracias. Para orientarte mejor necesito algunos datos: ¿cuál es tu nombre completo, tu edad y tu ciudad? |  |
| Make: |  | campos_actualizar={consentimiento_datos:true, consentimiento_servicio:true, consentimiento_investigacion:true, timestamp_consentimiento:2026-03-20T10:32:00}. |  |
| Sheets: |  | PACIENTES: todos los consentimientos=TRUE. timestamp_consentimiento registrado. |  |
|  |  |  |  |

|  | Turno 4  [F1 — Aseguramiento] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | María Torres, 38 años, Medellín. |  |
| Agente: |  | Mucho gusto, María. ¿Tienes medicina prepagada o pagas de forma particular? |  |
| Make: |  | campos_actualizar={nombre:'María Torres', edad:38, ciudad:'Medellín'}. |  |
| Sheets: |  | PACIENTES: nombre, edad, ciudad actualizados. |  |
|  |  |  |  |

|  | Turno 5  [F1 → F2 → F3] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Prepagada Sura. |  |
| Agente: |  | Perfecto. Atendemos programas de Cefalea, Epilepsia, Sueño, Memoria y más. Dado lo que mencionas, comenzaremos con la evaluación de riesgo neurológico para cefalea — esto nos permitirá orientarte de la mejor forma. ¿Comenzamos? |  |
| Make: |  | campos_actualizar={aseguramiento:'Prepagada', entidad_prepagada:'Sura', programa_clinico:'Cefalea', fase_actual:'F3'}. EPS habría generado fase_siguiente=ADMIN con link. |  |
| Sheets: |  | PACIENTES: aseguramiento=Prepagada, programa_clinico=Cefalea, fase_actual=F3. |  |
|  |  |  |  |

|  | Turno 6  [F3 — D1 + D2] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Sí, claro. |  |
| Agente: |  | Gracias. Primer grupo de preguntas: ¿El dolor es pulsátil (como latidos) o sientes una presión constante? ¿Y en qué zona de la cabeza lo sientes principalmente? |  |
| Make: |  | F3 iniciada. Dominio D1 activado. score_total=0 hasta respuesta. |  |
| Sheets: |  | PACIENTES: sin cambios aún en score. |  |
|  |  |  |  |

|  | Turno 7  [F3 — D1 ✓, D2] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Es pulsátil, en el lado derecho. A veces me da náuseas también. |  |
| Agente: |  | Entiendo. ¿Ha tenido junto con estos dolores: fiebre, vómito en proyectil, visión doble, pérdida de fuerza o el peor dolor de su vida de inicio súbito? |  |
| Make: |  | D1=+2 (pulsátil unilateral, ICHD-3 Criterio B). D2 activado. campos_actualizar={score_total:2, respuestas_orientacion:{D1:'pulsatil_derecho', D2:'pendiente'}}. |  |
| Sheets: |  | PACIENTES: score_total=2. |  |
|  |  |  |  |

|  | Turno 8  [F3 — D2 ✓, D3] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | No, nada de eso. Solo las náuseas. |  |
| Agente: |  | Bien. ¿Cuántas veces a la semana le dan estos dolores aproximadamente? ¿Y desde hace cuánto tiempo tiene este problema? |  |
| Make: |  | D2=+1 (náuseas, sin banderas rojas). score_total=3. flag_alarma=false. D3 activado. |  |
| Sheets: |  | PACIENTES: score_total=3. flag_alarma=false. |  |
|  |  |  |  |

|  | Turno 9  [F3 — D3 ✓, D4] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Unas 3 o 4 veces a la semana, llevo como 3 meses así. |  |
| Agente: |  | Eso es bastante frecuente y entiendo lo difícil que debe ser. Del 0 al 10, ¿qué tanto le afectan estos dolores en su vida diaria — trabajo, actividades, descanso? |  |
| Make: |  | D3=+3 (≥3/semana, 3 meses — ICHD-3 Criterio A: >15 días/mes en el umbral). score_total=6. |  |
| Sheets: |  | PACIENTES: score_total=6. |  |
|  |  |  |  |

|  | Turno 10  [F3 — D4 ✓, D5] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Un 7, hay días que no puedo ni trabajar. |  |
| Agente: |  | Entiendo. Cuando tiene el dolor, ¿es sensible a la luz brillante o a los ruidos fuertes? |  |
| Make: |  | D4=+3 (7/10, limitación laboral — ICHD-3 Criterio C: agravación con actividad). score_total=9. |  |
| Sheets: |  | PACIENTES: score_total=9. |  |
|  |  |  |  |

|  | Turno 11  [F3 — D5 ✓, D6] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Sí, a los dos. Tengo que cerrar las persianas y todo. |  |
| Agente: |  | ¿Ha tomado algún medicamento para estos dolores? ¿Le ha funcionado bien? |  |
| Make: |  | D5=+2 (fotofobia + fonofobia — ICHD-3 Criterio C). score_total=11. |  |
| Sheets: |  | PACIENTES: score_total=11. |  |
|  |  |  |  |

|  | Turno 12 — CLASIFICACIÓN  [F3 → F4 + Reporte visual] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Solo ibuprofeno pero casi no me hace nada. |  |
| Agente: |  | María, gracias por toda la información. Con base en tu evaluación de riesgo, esto sugiere un nivel de RIESGO ALTO neurológico, compatible con migraña episódica de alta frecuencia. El especialista neurólogo podrá confirmar y definir el manejo más adecuado. En un momento recibirás tu reporte de evaluación. ¿Te cuento sobre las opciones de seguimiento? |  |
| Make: |  | D6=+2 (ibuprofeno sin efecto). score_total=13. nivel_riesgo=Alto. fenotipo='Migraña episódica alta frecuencia'. guia_soporte='ICHD-3 G43.009'. cie10='G43.009'. Escenario 2 activado → genera imagen reporte → envía por WhatsApp. Fila insertada en COHORTES_INVESTIGACION. |  |
| Sheets: |  | PACIENTES: score_total=13, nivel_riesgo=Alto, guia_soporte=ICHD-3, cie10=G43.009, reporte_enviado=TRUE, fecha_ultima_orientacion=2026-03-20. COHORTES: nueva fila anonimizada. |  |
|  |  |  |  |

|  | Turno 13 — REPORTE VISUAL  [F3 — Imagen automática] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | [Recibe imagen del reporte] |  |
| Agente: |  | [IMAGEN: Reporte de Evaluación de Riesgo Neurológico ICN Salud — Programa: Cefalea — Nivel de riesgo: ALTO — Fenotipo probable: Migraña episódica de alta frecuencia — Recomendación: Evaluación con especialista neurólogo — AVISO: Este resultado corresponde a una evaluación de riesgo y no constituye un diagnóstico médico] |  |
| Make: |  | Escenario 2 completado. Imagen generada con branding ICN + disclaimer legal. reporte_enviado=TRUE. |  |
| Sheets: |  | PACIENTES: reporte_enviado=TRUE. |  |
|  |  |  |  |

|  | Turno 14 — CONVERSIÓN  [F4 → F5] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Sí, cuéntame. ¿Cuánto vale? |  |
| Agente: |  | El Paquete Diagnóstico de Cefalea incluye consulta con neurólogo especialista y valoración completa. María, llevas 3 meses con dolores que te limitan el trabajo — una evaluación temprana evita que el problema avance. Tenemos disponibilidad esta semana. ¿Te quedaría bien el jueves o el viernes? |  |
| Make: |  | F4 activada. Objeción de precio manejada con argumento clínico. Make consulta Google Calendar → slots disponibles jueves y viernes. campos_actualizar={conversion:'Paquete cefalea', canal_agenda:'Directo', fase_actual:'F5'}. Nueva fila en CITAS. |  |
| Sheets: |  | PACIENTES: conversion=Paquete cefalea, canal_agenda=Directo, fase_actual=F5. CITAS: nueva fila con fecha pendiente confirmación. |  |
|  |  |  |  |

9.1 Estado final en Google Sheets

| Hoja | Campo | Valor final |
| --- | --- | --- |
| PACIENTES | nombre | María Torres |
| PACIENTES | aseguramiento | Prepagada — Sura |
| PACIENTES | consentimientos | TRUE (datos + servicio + investigación) |
| PACIENTES | fase_actual | F5 |
| PACIENTES | programa_clinico | Cefalea |
| PACIENTES | guia_soporte | ICHD-3 — G43.009 Migraña episódica alta frecuencia |
| PACIENTES | cie10 | G43.009 |
| PACIENTES | nivel_riesgo | Alto |
| PACIENTES | score_total | 13 |
| PACIENTES | fenotipo_probable | Migraña episódica de alta frecuencia |
| PACIENTES | respuestas_orientacion | JSON D1–D6 guardado |
| PACIENTES | reporte_enviado | TRUE |
| PACIENTES | conversion | Paquete diagnóstico cefalea |
| PACIENTES | canal_agenda | Directo |
| PACIENTES | fecha_ultima_orientacion | 2026-03-20 |
| PACIENTES | cohorte | Cefalea_Alto_MigrañaFrecuente |
| CONVERSACIONES | turnos registrados | 14 turnos con guia_soporte por turno |
| CITAS | estado | Pendiente confirmación de fecha |
| COHORTES_INVESTIGACION | fila anonimizada | Insertada con todos los campos clínicos |

10. Capa de Investigación Clínica

NeurOrientador no es solo un flujo conversacional. Está estructurado como un sistema de recolección de evidencia clínica propia de ICN Salud. Esta capa permite análisis longitudinal, identificación de patrones y base para publicaciones científicas.

10.1 Variables clínicas estructuradas recolectadas

| Variable | Fuente | Tipo | Uso en investigación |
| --- | --- | --- | --- |
| Programa clínico | F1 — selección paciente | Categórica | Segmentación de cohortes por área neurológica |
| Nivel de riesgo | F3 — scoring | Ordinal (Bajo/Mod/Alto/Alarma) | Distribución de riesgo poblacional ICN |
| Score total | F3 — suma D1-D6 | Numérica continua | Análisis de correlación con desenlaces |
| Fenotipo probable | F3 — clasificación | Categórica | Prevalencia de fenotipos por programa |
| CIE-10 | F3 — asignación automática | Código estandarizado | Interoperabilidad con sistemas de salud |
| Guía soporte | F3 — trazabilidad | Texto estructurado | Auditoría metodológica y validación |
| Respuestas D1–D6 | F3 — árbol completo | JSON estructurado | Análisis de patrones de síntomas |
| Tiempo F1 → conversión | Timestamp F1 vs. F4 | Numérica (días) | Optimización del embudo de conversión |
| Adherencia F5–F6 | Respuestas a recordatorios | Booleana por turno | Tasa de seguimiento y adherencia |
| Reorientación cada 6 meses | fecha_ultima_orientacion | Fecha | Seguimiento longitudinal de evolución de riesgo |

10.2 Clasificación automática por cohortes

| Formato del campo cohorte (autogenerado por Make al completar F3) |
| --- |
| Estructura: {programa}_{riesgo}_{fenotipo_abreviado} |
|  |
| Ejemplos: |
| Cefalea_Alto_MigrañaFrecuente |
| Epilepsia_Moderado_CrisisGeneralizada |
| Sueño_Bajo_InsomnioLeve |
| Neurodesarrollo_Alto_TDAH |
|  |
| Este campo permite filtrar y analizar cohortes directamente en Google Sheets |
| sin procesamiento adicional. Es la base para los análisis de investigación ICN. |

10.3 Resultados esperados de la capa de investigación

Evidencia clínica propia ICN: datos reales de pacientes colombianos con validación metodológica (ICHD-3, DSM-5-TR, Guías ICN).

Optimización de protocolos: identificación de preguntas con mayor valor predictivo para ajustar el árbol clínico de F3.

Base para publicaciones científicas: cohortes estructuradas con CIE-10, guía soporte y seguimiento longitudinal.

Análisis con IA (V2): módulo de ChatGPT sobre COHORTES_INVESTIGACION para identificar patrones y optimizar rutas clínicas automáticamente.

11. Reporte Visual de Riesgo — Entrega al Paciente

Al finalizar F3 (o al transitar a F4), el sistema genera automáticamente una imagen de reporte clínico y la envía por WhatsApp. Este reporte es obligatorio y no puede omitirse.

11.1 Contenido obligatorio del reporte visual

| Elemento | Contenido | Obligatorio |
| --- | --- | --- |
| Encabezado | Logo ICN Salud + nombre 'NeurOrientador' + fecha de evaluación | Sí |
| Nombre del paciente | Nombre capturado en F1 | Sí |
| Programa evaluado | Nombre del programa clínico (ej: Cefalea) | Sí |
| Nivel de riesgo | Bajo / Moderado / Alto / Alarma — con color indicador | Sí |
| Fenotipo probable | Descripción del fenotipo (sin diagnóstico definitivo) | Sí |
| Guía base | Guía clínica que soportó la clasificación | Sí |
| Recomendación | Paso siguiente recomendado (consulta especialista) | Sí |
| Disclaimer legal | 'Este resultado corresponde a una evaluación de riesgo y no constituye un diagnóstico médico' — texto completo obligatorio | Sí — nunca puede omitirse |
| Pie de página | ICN Salud + Teleorientación en Salud Neurológica + contacto | Sí |

11.2 Implementación técnica del reporte

| Opciones de implementación para generación de imagen en Make |
| --- |
| OPCIÓN A — Bannerbear API (recomendada para V1): |
| Crear template en Bannerbear con branding ICN. |
| Make llama a la API de Bannerbear con los datos del paciente. |
| Bannerbear genera la imagen y devuelve URL. |
| Make envía la imagen por WhatsApp usando la URL. |
|  |
| OPCIÓN B — HTML-to-Image API (más flexible): |
| Make construye un HTML con los datos del paciente. |
| Llama a una API de HTML-to-image (ej: hcti.io, htmlcsstoimage). |
| Obtiene la URL de la imagen generada. |
| Envía por WhatsApp. |
|  |
| OPCIÓN C — Google Slides/Docs API (integración nativa Google): |
| Template en Google Slides. Make llena los campos con datos. |
| Exporta como imagen PNG. Envía por WhatsApp. |
|  |
| En todos los casos: el disclaimer legal es un texto fijo no editable. |

12. Escalamiento Obligatorio a Humano

El escalamiento a neuroasesor humano es obligatorio en los siguientes casos. Make ejecuta la notificación automáticamente cuando flag_alarma = TRUE o fase_siguiente = HUMANO.

| Trigger | Descripción | Acción de Make | Mensaje al paciente |
| --- | --- | --- | --- |
| Signo de alarma clínica | ChatGPT detecta: cefalea en trueno, FAST positivo, pérdida de consciencia, convulsión activa, fiebre + rigidez de nuca, pensamiento suicida | flag_alarma=TRUE → WhatsApp a neuroasesor interno con: nombre, teléfono, síntoma exacto, fase, guia_soporte | Informar que va a recibir atención especializada. En casos urgentes: indicar ir a urgencias. |
| Duda clínica | IA no puede clasificar con certeza el caso según las guías disponibles | fase_siguiente=HUMANO en respuesta JSON | Informar que un especialista de ICN lo contactará pronto. |
| Solicitud del paciente | Paciente pide explícitamente hablar con una persona | fase_siguiente=HUMANO | Confirmar que se conecta con el equipo ICN. |
| EPS detectada | Paciente menciona ser usuario de EPS | fase_siguiente=ADMIN → link icnsalud.com/#contacto | Redirigir al canal correcto con el link. |
| Resultado postconsulta — externo | En F5, paciente tiene órdenes o exámenes de fuera de ICN | fase_siguiente=HUMANO para gestión por asesor | Informar que un asesor lo apoyará con los próximos pasos. |

13. Puntos Críticos y Riesgos de Producción

| Riesgo | Descripción | Mitigación |
| --- | --- | --- |
| JSON inválido de ChatGPT | Si la IA genera texto libre en lugar de JSON, Make falla al parsear. | Módulo de validación JSON en Make. Si falla: retry con prompt de corrección. Máx 2 reintentos. Si persiste: escalamiento a HUMANO. |
| Lenguaje de diagnóstico | ChatGPT puede usar frases como 'Tienes X' si el prompt no es suficientemente estricto. | El prompt base incluye regla explícita y ejemplos de lenguaje prohibido. Auditoría aleatoria de conversaciones cada semana. |
| Historial JSON largo | Conversaciones largas elevan costo y pueden exceder contexto de GPT-4o. | Máximo 20 turnos en historial_json. Truncar los más antiguos automáticamente. |
| Alarma clínica no detectada | IA puede pasar por alto bandera roja si el usuario la describe de forma indirecta. | Filtro adicional en Make ANTES de llamar a ChatGPT: búsqueda de keywords de alarma en el mensaje bruto. |
| Reporte visual no generado | Si el Escenario 2 falla, el paciente no recibe su reporte. | Reintentar automáticamente 2 veces. Si falla: notificar al equipo ICN para envío manual. Registrar en Sheets. |
| Omisión de F3 | Agente salta F3 si el prompt de F2 no está bien configurado. | F2 siempre debe tener fase_siguiente=F3. Validar en Make antes de ejecutar ChatGPT. |
| Acceso no autorizado a Sheets | Google Sheets con datos de salud expuestos. | Solo cuentas @icnsalud.com con 2FA. Make accede con cuenta de servicio de permisos mínimos. Auditoría mensual. |
| Costos API crecientes | Alto volumen puede elevar costos de GPT-4o. | Monitorear tokens/mes. Si supera presupuesto: F5 y F6 con mensajes estáticos, IA solo en F1–F4. |
| Paciente existente en nuevo número | Si paciente cambia de número, se crea registro duplicado. | V1: aceptar como limitación. V2: identificación por nombre + fecha de nacimiento como clave adicional. |



---

# FUENTE V1: NeuroOrientador V1 (1).docx

**Rol de esta fuente:** Primera especificación técnica; referencia histórica.


NeurOrientador

ICN Salud — Agente Conversacional Clínico-Comercial

Documentación Técnica de Implementación — Versión 1.0

Stack: WhatsApp Business API  ·  Make ·  ChatGPT API  ·  Google Sheets

2026

| Canal WhatsApp Business API | Automatización Make | IA ChatGPT API (GPT-4o) | Datos Google Sheets |
| --- | --- | --- | --- |

1. Arquitectura Técnica del Sistema

NeurOrientador es un sistema conversacional modular que combina tres capas tecnológicas integradas entre sí: la capa de canal (WhatsApp), la capa de automatización y orquestación (Make), y la capa de inteligencia artificial (ChatGPT API). Los datos del paciente se presentan en Google Sheets como base de datos operativa.

Diagrama de componentes

| Flujo de datos — Componentes principales |
| --- |
| USUARIO (WhatsApp) → envia mensaje |
| ↓ |
| WHATSAPP BUSINESS API → webhook dispara evento HTTP POST a Make |
| ↓ |
| MAKE — Escenario principal: recibe mensaje, recupera historial, construye contexto |
| ↓ |
| CHATGPT API (GPT-4o) → procesa contexto + prompt de fase activa → genera respuesta |
| ↓ |
| MAKE — Parsea respuesta JSON de IA, actualiza Google Sheets, envía respuesta a WhatsApp |
| ↓ |
| USUARIO (WhatsApp) → recibe respuesta del agente |

Stack tecnológico detallado

| Componente | Herramienta | Rol en el sistema | Consideraciones |
| --- | --- | --- | --- |
| Canal | WhatsApp Business API | Recibir y enviar mensajes al paciente | Requiere número verificado y cuenta Meta Business |
| Orquestador | Make | Conectar todos los módulos, gestionar el flujo, enrutar fases | Escenario activo 24/7, webhook siempre abierto |
| Inteligencia artificial | ChatGPT API — GPT-4o | Procesar mensajes, aplicar lógica de fase, generar respuestas | Se envía historial completo de la conversación en cada llamada |
| Base de datos | Google Sheets | Almacenar pacientes, historial, fase activa, scores, citas | Una hoja por entidad: Pacientes, Conversaciones, Citas |
| Historial conversacional | Google Sheets (col. JSON) | Persistir mensajes anteriores para contexto de IA | Columna 'historial' con array JSON stringificado |
| Notificaciones humano | WhatsApp / Email via Make | Alertar a neuroasesor cuando se requiere intervención | Filtro de alarma activa transferencia automática |

2. Esquema de Datos — Google Sheets

El sistema utiliza tres hojas de cálculo dentro de un mismo Google Sheets. Cada hoja representa una entidad del sistema. Los campos están diseñados para ser escritos y leídos directamente por Make en cada turno de conversación.

2.1 Hoja 1: PACIENTES

Una fila por paciente. Se crea en Fase 1. Se actualiza en cada fase posterior.

| Campo | Tipo | Descripción | Ejemplo |
| --- | --- | --- | --- |
| paciente_id | Texto (auto) | ID único generado por Make al crear fila | PAC-20260320-001 |
| telefono | Texto | Número WhatsApp del paciente (clave primaria) | 573001234567 |
| nombre | Texto | Nombre capturado en Fase 1 | María Torres |
| edad | Número | Edad en años | 38 |
| ciudad | Texto | Ciudad de residencia | Medellín |
| aseguramiento | Texto | Particular / Prepagada / (EPS se redirige a icnsalud.com/#contacto | Prepagada |
| entidad_prepagada | Texto | Nombre de la prepagada si aplica | Sura |
| fase_actual | Texto | Fase activa del agente | F3 |
| programa_clinico | Texto | Programa neurológico asignado | Cefalea |
| nivel_riesgo | Texto | Bajo / Moderado / Alto / Alarma | Alto |
| score_total | Número | Puntaje total del scoring F3 | 12 |
| fenotipo_probable | Texto | Fenotipo clínico probable | Migraña episódica frecuente |
| conversion | Texto | Tipo de conversión lograda | Paquete diagnóstico cefalea |
| fecha_cita | Fecha | Fecha de la cita agendada | 2026-03-26 |
| estado_cita | Texto | Pendiente / Confirmada / Asistió / No asistió | Confirmada |
| fecha_creacion | Fecha | Timestamp de primer contacto | 2026-03-20T10:30:00 |
| ultima_actividad | Fecha | Timestamp del último mensaje | 2026-03-20T11:15:00 |
| requiere_humano | Booleano | TRUE si se activó transferencia a asesor | FALSE |
| notas_internas | Texto | Campo libre para equipo clínico | Historial familiar migraña |
| respuestas_orientacion | JSON (texto) | Respuestas del paciente a los 6 dominios del árbol de teleorientacion (D1-D6), guardadas como JSON stringficado. Permite auditar el scoring y reconstruir el razonamiento clínico. | {“D1_confirmacion”:”pulsatil derecho”,”D2_alarma”:”nauseas”,”D3_frecuencia”:”3-4/semana”,”D4_severidad”:”7/10”,”D5_fenotipo”:”luz y ruido”,”D6_medicamento”:”ibuprofeno sin efecto”} |

2.2 Hoja 2: CONVERSACIONES

Una fila por turno de conversación. Permite auditoría completa y reconstrucción de contexto.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| conv_id | Texto (auto) | ID único del turno: CONV-{paciente_id}-{timestamp} |
| paciente_id | Texto | Referencia al paciente (FK) |
| telefono | Texto | Número WhatsApp (para lookup rápido) |
| fase | Texto | Fase activa en ese turno (F0 a F6) |
| mensaje_usuario | Texto | Mensaje exacto enviado por el paciente |
| respuesta_agente | Texto | Respuesta generada por ChatGPT y enviada |
| timestamp | Fecha | Fecha y hora exacta del turno |
| tokens_usados | Número | Tokens consumidos en la llamada API |
| flag_alarma | Booleano | TRUE si el turno activó bandera roja clínica |

2.3 Hoja 3: CITAS

Una fila por cita o paquete convertido. Alimenta el seguimiento de Fase 5.

| Campo | Tipo | Descripción |
| --- | --- | --- |
| cita_id | Texto (auto) | ID único de la cita |
| paciente_id | Texto | Referencia al paciente |
| tipo | Texto | Consulta / Paquete diagnóstico / Tratamiento |
| programa | Texto | Programa clínico asociado |
| fecha_cita | Fecha | Fecha programada |
| hora_cita | Texto | Hora programada |
| recordatorio_3d | Booleano | TRUE si ya se envió recordatorio -3 días |
| recordatorio_1d | Booleano | TRUE si ya se envió recordatorio -1 día |
| confirmacion | Texto | Pendiente / Confirmada / Cancelada |
| seguimiento_post | Booleano | TRUE si ya se realizó seguimiento postconsulta |
| resultado_post | Texto | Medicamentos / Terapias / Exámenes / Sin novedad |

2.4 Campo clave: historial_json (en hoja PACIENTES)

| Campo historial_json — Estructura |
| --- |
| Este campo en la hoja PACIENTES almacena el historial de conversación |
| como un array JSON stringificado. Make lo lee, lo pasa a ChatGPT, |
| y luego actualiza el campo con el nuevo turno agregado. |
|  |
| Ejemplo de contenido del campo: |
| [{"role":"user","content":"Hola tengo dolor de cabeza"}, |
| {"role":"assistant","content":"Hola María, soy NeurOrientador..."}, |
| {"role":"user","content":"Es pulsátil y muy fuerte"}, |
| {"role":"assistant","content":"Entiendo, ¿con qué frecuencia..."}] |
|  |
| Límite recomendado: mantener los últimos 20 turnos para controlar tokens. |

3. Flujos de Make — Escenarios de Automatización

El sistema se implementa en Make con 3 escenarios separados. Cada escenario tiene un propósito específico y se activa por un trigger distinto.

3.1 Escenario 1: Conversación principal (webhook)

Este es el escenario central. Se activa cada vez que el paciente envía un mensaje. Es el motor de todo el sistema.

| Trigger: Webhook HTTP → WhatsApp Business API |
| --- |
| El número de WhatsApp de ICN Salud tiene configurado un webhook que apunta |
| a la URL del escenario en Make. Cada mensaje entrante dispara este escenario. |

| 1 | [Webhook]  Recibir mensaje de WhatsApp Parsear: numero_telefono, mensaje_texto, timestamp del cuerpo JSON del webhook de WhatsApp Business API |
| --- | --- |

| 2 | [Google Sheets — Buscar fila]  Buscar paciente por teléfono Filtro: columna 'telefono' = numero_recibido. Si no existe → ir al paso 3a. Si existe → ir al paso 3b |
| --- | --- |

| 3a | [Google Sheets — Crear fila]  Crear nuevo paciente Insertar fila en hoja PACIENTES con: telefono, fecha_creacion, fase_actual = 'F0', historial_json = '[]' |
| --- | --- |

| 3b | [Google Sheets — Leer fila]  Leer datos del paciente existente Recuperar: fase_actual, historial_json, programa_clinico, nivel_riesgo, nombre, score_total |
| --- | --- |

| 4 | [Herramienta — JSON Parse]  Deserializar historial Convertir el string JSON del campo historial_json a array de objetos para enviarlo a ChatGPT |
| --- | --- |

| 5 | [ChatGPT — Create Completion]  Llamar a la API de ChatGPT Model: gpt-4o \| Max tokens: 800 \| Messages: [system_prompt_fase + historial + mensaje_actual_usuario] |
| --- | --- |

| 6 | [Herramienta — JSON Parse]  Parsear respuesta estructurada de IA La IA responde siempre en JSON con campos: respuesta_visible, fase_siguiente, campos_actualizar, flag_alarma |
| --- | --- |

| 7 | [Google Sheets — Actualizar fila]  Actualizar datos del paciente Escribir: fase_actual, programa_clinico, nivel_riesgo, score_total, ultima_actividad, requiere_humano y todos los campos_actualizar del JSON |
| --- | --- |

| 8 | [Google Sheets — Crear fila]  Registrar turno en CONVERSACIONES Insertar nuevo registro con: paciente_id, fase, mensaje_usuario, respuesta_agente, timestamp, flag_alarma |
| --- | --- |

| 9 | [Herramienta — Array Push]  Actualizar historial JSON Agregar {'role':'user','content':mensaje} y {'role':'assistant','content':respuesta} al array, mantener últimos 20 turnos |
| --- | --- |

| 10 | [Google Sheets — Actualizar fila]  Persistir historial actualizado Escribir el array actualizado como string JSON en campo historial_json del paciente |
| --- | --- |

| 11 | [Router — Condicional]  Verificar flag_alarma Si flag_alarma = TRUE → ejecutar rama de alarma (paso 12). Si FALSE → paso 13 |
| --- | --- |

| 12 | [WhatsApp — Enviar mensaje (asesor)]  Notificar a neuroasesor humano Enviar al número interno del equipo: nombre paciente, teléfono, síntoma de alarma, resumen clínico |
| --- | --- |

| 13 | [WhatsApp — Enviar mensaje (paciente)]  Enviar respuesta al paciente Enviar el campo 'respuesta_visible' del JSON al número de WhatsApp del paciente |
| --- | --- |

3.2 Escenario 2: Recordatorios y seguimiento (programado)

Este escenario se ejecuta automáticamente cada día a las 8:00 AM. Revisa la hoja CITAS y envía recordatorios o seguimientos según corresponda.

| Trigger: Schedule → diariamente a las 8:00 AM |
| --- |
| No requiere interacción del usuario. Make consulta Google Sheets de forma proactiva. |

| 1 | [Schedule]  Trigger programado diario Ejecutar todos los días a las 08:00 AM (zona horaria Colombia — UTC-5) |
| --- | --- |

| 2 | [Google Sheets — Buscar filas]  Obtener citas del período Filtrar hoja CITAS: fecha_cita entre hoy-3d y hoy+1d, estado_cita != 'Asistió' |
| --- | --- |

| 3 | [Iterator]  Iterar sobre citas encontradas Procesar cada cita por separado en los pasos siguientes |
| --- | --- |

| 4 | [Router — Condicional (fecha)]  Determinar tipo de recordatorio Si fecha = hoy+3 y recordatorio_3d=FALSE → enviar recordatorio -3d. Si fecha = hoy+1 y recordatorio_1d=FALSE → enviar recordatorio -1d |
| --- | --- |

| 5a | [WhatsApp — Enviar mensaje]  Enviar recordatorio 3 días antes Mensaje: nombre, fecha/hora cita, programa, instrucciones de preparación |
| --- | --- |

| 5b | [WhatsApp — Enviar mensaje]  Enviar recordatorio 1 día antes Mensaje: confirmación de asistencia con opciones Sí/No como botones o texto |
| --- | --- |

| 6 | [Google Sheets — Actualizar fila]  Marcar recordatorio enviado Actualizar campo recordatorio_3d o recordatorio_1d a TRUE para no re-enviar |
| --- | --- |

| 7 | [Google Sheets — Buscar filas]  Obtener citas de ayer (postconsulta) Filtrar citas con fecha = ayer y seguimiento_post = FALSE y estado_cita = 'Confirmada' |
| --- | --- |

| 8 | [WhatsApp — Enviar mensaje]  Enviar mensaje de seguimiento post Preguntar cómo le fue en la consulta, solicitar órdenes/resultado, ofrecer siguiente paso |
| --- | --- |

| 9 | [Google Sheets — Actualizar fila]  Marcar seguimiento enviado Actualizar seguimiento_post = TRUE en hoja CITAS |
| --- | --- |

3.3 Escenario 3: Seguimiento preventivo — Fase 6 (programado)

Este escenario gestiona el programa educativo de Fase 6. Se ejecuta cada 2 días para los pacientes activos en esa fase.

| Trigger: Schedule → cada 2 días a las 9:00 AM |
| --- |
| Activo para pacientes con fase_actual = F6. Envía la tríada: educación + acción + pregunta. |

| 1 | [Schedule]  Trigger programado cada 2 días Ejecutar lunes, miércoles y viernes a las 09:00 AM |
| --- | --- |

| 2 | [Google Sheets — Buscar filas]  Obtener pacientes en Fase 6 Filtrar hoja PACIENTES: fase_actual = 'F6' |
| --- | --- |

| 3 | [Iterator]  Iterar sobre pacientes F6 Procesar cada paciente individualmente |
| --- | --- |

| 4 | [ChatGPT — Create Completion]  Generar mensaje educativo personalizado System prompt F6 + datos del paciente (programa, riesgo, último mensaje). Generar tríada: educación + acción + pregunta |
| --- | --- |

| 5 | [WhatsApp — Enviar mensaje]  Enviar mensaje preventivo Enviar el mensaje educativo generado por IA al paciente |
| --- | --- |

| 6 | [Google Sheets — Actualizar fila]  Registrar envío Actualizar ultima_actividad en hoja PACIENTES |
| --- | --- |

4. Prompts de ChatGPT por Fase

Cada fase tiene su propio system prompt. En Make, el prompt se selecciona dinámicamente según el valor del campo fase_actual del paciente. Los prompts están diseñados para que ChatGPT responda SIEMPRE en formato JSON estructurado para que Make pueda procesarlo.

| Formato de respuesta JSON obligatorio para todas las fases |
| --- |
| ChatGPT debe responder SIEMPRE con este JSON (sin texto adicional): |
| { |
| "respuesta_visible": "Texto que se enviará al paciente por WhatsApp", |
| "fase_siguiente": "F1", |
| "campos_actualizar": { |
| "nombre": "María Torres", |
| "programa_clinico": "Cefalea", |
| "nivel_riesgo": "Alto", |
| "score_total": 12 |
| }, |
| "flag_alarma": false, |
| "notas_internas": "Migraña episódica frecuente probable. Sin banderas rojas." |
| } |
|  |
| Solo incluir en campos_actualizar los campos que cambian en ese turno. |

4.1 Prompt Base — Sistema (incluir en todas las fases)

| 🔷 SYSTEM PROMPT BASE — Insertar al inicio de cada prompt de fase Eres NeurOrientador, el asistente de teleorientación clínica de ICN Salud. Tu rol es guiar a los pacientes a través de un proceso de orientación neurológica estructurado por fases. Eres amable, profesional y empático. REGLA ABSOLUTA: Responde SIEMPRE en formato JSON válido con esta estructura: { "respuesta_visible": "...", "fase_siguiente": "F0\|F1\|F2\|F3\|F4\|F5\|F6\|ADMIN\|HUMANO", "campos_actualizar": {}, "flag_alarma": false, "notas_internas": "..." } NUNCA emitas diagnóstico definitivo. NUNCA uses lenguaje alarmista innecesario. SIEMPRE escala a HUMANO si detectas: pensamiento suicida, dolor torácico, pérdida de consciencia, convulsión activa, ACV probable. Datos actuales del paciente: - Nombre: {{nombre}} \| Edad: {{edad}} \| Ciudad: {{ciudad}} - Aseguramiento: {{aseguramiento}} \| Fase actual: {{fase_actual}} - Programa: {{programa_clinico}} \| Riesgo previo: {{nivel_riesgo}} |
| --- |

4.2 Prompt Fase 0 — Clasificación inicial

| 🔷 PROMPT FASE 0 {{SYSTEM_PROMPT_BASE}} FASE ACTUAL: F0 — Clasificación del motivo de contacto. Tu tarea: analizar el primer mensaje del usuario y clasificarlo. REGLAS DE CLASIFICACIÓN: - Si menciona síntomas, enfermedades, dolor, problemas neurológicos → fase_siguiente: F1 - Si menciona EPS, autorización, historia clínica, resultado → fase_siguiente: ADMIN - Si pregunta solo por precio sin contexto clínico → fase_siguiente: F1 (capturar datos primero) - Si es prepagada o particular con interés clínico → fase_siguiente: F1 En respuesta_visible: saluda brevemente y confirma que vas a ayudarle. En campos_actualizar: incluye solo lo que puedas inferir del mensaje inicial. Mensaje del usuario: {{mensaje_usuario}} |
| --- |

4.3 Prompt Fase 1 — Bienvenida e identificación

| 🔷 PROMPT FASE 1 {{SYSTEM_PROMPT_BASE}} FASE ACTUAL: F1 — Bienvenida, habeas data e identificación del paciente. Si es el primer contacto (nombre = vacío), haz lo siguiente en orden: 1. Presenta el aviso de habeas data brevemente: informa que los datos se tratan con confidencialidad según la Ley 1581 de 2012 y pide autorización. 2. Una vez autorizado, solicita: nombre completo, edad, ciudad y tipo de seguro. 3. Si menciona prepagada, solicitar nombre de la entidad. 4. Muestra brevemente los programas disponibles: Cefalea, Epilepsia, Sueño, Memoria, Movimiento, ACV, Parálisis facial, Neurodesarrollo, Dolor neuropático. 5. Pregunta cuál describe mejor su situación. NO hagas preguntas clínicas en esta fase. Solo captura datos de identificación. MÁXIMO 2 preguntas por turno. Sé conversacional, no uses formularios. Cuando tengas: nombre, edad, ciudad y aseguramiento → fase_siguiente: F2 Actualiza campos_actualizar con cada dato que el usuario confirme. |
| --- |

4.4 Prompt Fase 2 — Identificación de necesidad

| 🔷 PROMPT FASE 2 {{SYSTEM_PROMPT_BASE}} FASE ACTUAL: F2 — Identificar exactamente qué necesita el usuario. Datos disponibles del paciente: nombre={{nombre}}, programa={{programa_clinico}} Tu tarea: determinar con una o dos preguntas si el usuario busca: A) Orientación clínica (entender qué le pasa) → fase_siguiente: F3 B) Agendar cita directamente → fase_siguiente: F4 C) Trámite administrativo → fase_siguiente: ADMIN Si hay ambigüedad (quiere orientación Y cita): ir a F3 primero. En campos_actualizar: registra motivo_contacto con A, B o C. Sé breve. Esta fase debe resolverse en máximo 2 turnos. |
| --- |

4.5 Prompt Fase 3 — Teleorientación neurológica

| 🔷 PROMPT FASE 3 — NÚCLEO CLÍNICO {{SYSTEM_PROMPT_BASE}} FASE ACTUAL: F3 — Teleorientación neurológica estructurada. Programa activo: {{programa_clinico}} \| Score acumulado: {{score_total}} Debes recorrer 6 dominios conversacionales en orden. Haz MÁXIMO 1-2 preguntas por turno. Acumula el score en cada respuesta. DOMINIOS Y SCORING (programa: Cefalea — adaptar para otros programas): D1 CONFIRMACIÓN: ¿El dolor es pulsátil o en presión? ¿En qué parte de la cabeza? Score: pulsátil unilateral +2 \| bilateral o en presión +1 D2 ALARMA: ¿Tiene fiebre, vómito en proyectil, visión doble, pérdida de fuerza? Score: ninguno +0 \| uno presente +1 \| dos o más → flag_alarma: true D3 CARACTERIZACIÓN: ¿Cuántas veces por semana? ¿Desde hace cuánto? Score: <1/semana +1 \| 1-2/semana +2 \| 3+/semana +3 D4 SEVERIDAD: ¿Del 0 al 10, cuánto le afecta la vida diaria? Score: 1-4 +1 \| 5-7 +2 \| 8-10 +3 D5 FENOTIPO: ¿Hay sensibilidad a la luz, al ruido, náuseas? Score: uno +1 \| dos +2 \| todos +3 D6 SALIDA: ¿Ha tomado medicamento? ¿Qué tan efectivo fue? Score: sin medicamento +1 \| poco efecto +2 \| sin efecto +3 CLASIFICACIÓN FINAL (suma todos los dominios, máx 15): 0-4: nivel_riesgo = Bajo → fase_siguiente: F6 5-8: nivel_riesgo = Moderado → fase_siguiente: F4 9-12: nivel_riesgo = Alto → fase_siguiente: F4 13-15 o flag_alarma=true: nivel_riesgo = Alarma → fase_siguiente: HUMANO Cuando hayas completado los 6 dominios: actualiza score_total, nivel_riesgo, fenotipo_probable en campos_actualizar y transita a la fase correspondiente. NUNCA digas diagnóstico. Usa lenguaje como 'esto sugiere', 'es posible que', 'el especialista podrá confirmar'. Sé clínico pero accesible. |
| --- |

4.6 Prompt Fase 4 — Conversión clínica

| 🔷 PROMPT FASE 4 {{SYSTEM_PROMPT_BASE}} FASE ACTUAL: F4 — Conversión clínica y comercial. Riesgo: {{nivel_riesgo}} \| Programa: {{programa_clinico}} \| Fenotipo: {{fenotipo_probable}} Tu tarea: convertir al paciente a una consulta o paquete diagnóstico. USA el nivel de riesgo como argumento clínico, no como amenaza. ESTRUCTURA DE LA CONVERSACIÓN F4: Turno 1: Resume brevemente los hallazgos ('Basándome en lo que me contaste...') Explica por qué es importante consultar con el especialista ahora. Turno 2: Presenta el paquete específico para su programa. Si no hay paquete activo, ofrecer consulta especializada. Turno 3: Si hay objeción de precio → resaltar costo de no tratar vs costo del paquete. Si hay objeción de tiempo → ofrecer horarios flexibles. Turno 4: Ofrecer agendar y preguntar disponibilidad de fecha. MANEJO DE OBJECIONES: - 'Es muy caro' → comparar con costo de tratamiento tardío, mencionar valor incluido - 'Ya fui al médico' → explicar valor del especialista neurólogo - 'Tengo miedo' → validar emoción, normalizar, enfocarse en solución - 'Quiero pensarlo' → respetar, ofrecer información adicional, acordar fecha de seguimiento Si el paciente pide hablar con una persona: fase_siguiente: HUMANO Si acepta agenda: actualizar conversion y fecha_cita, fase_siguiente: F5 Si rechaza completamente: fase_siguiente: F6 |
| --- |

4.7 Prompt Fase 5 — Seguimiento (usado en escenario 2)

| 🔷 PROMPT FASE 5 — Recordatorios y postconsulta {{SYSTEM_PROMPT_BASE}} FASE ACTUAL: F5 — Seguimiento de cita. Nombre: {{nombre}} \| Fecha cita: {{fecha_cita}} \| Programa: {{programa_clinico}} MODO: {{modo_f5}}  (valores posibles: recordatorio_3d \| recordatorio_1d \| postconsulta) Si modo = recordatorio_3d: Recordar amablemente la cita en 3 días. Dar indicaciones de preparación si aplica. Confirmar dirección o modalidad (presencial/virtual). Si modo = recordatorio_1d: Confirmar asistencia. Pedir que responda SÍ o NO. Si responde NO: ofrecer reprogramar, actualizar estado_cita = Cancelada. Si responde SÍ: actualizar estado_cita = Confirmada. Si modo = postconsulta: Preguntar cómo le fue. Preguntar si tiene órdenes médicas o fórmulas. Si tiene órdenes externas: fase_siguiente: HUMANO (asesor gestiona) Si tiene órdenes ICN: fase_siguiente: F4 (orientada a exámenes internos) Si sin novedad: fase_siguiente: F6 |
| --- |

4.8 Prompt Fase 6 — Prevención y comunidad

| 🔷 PROMPT FASE 6 {{SYSTEM_PROMPT_BASE}} FASE ACTUAL: F6 — Seguimiento preventivo, educación y remarketing. Programa: {{programa_clinico}} \| Riesgo: {{nivel_riesgo}} Tu tarea: enviar la TRÍADA de seguimiento: 1. EDUCACIÓN: Un dato breve y útil relacionado con el programa del paciente (máx 3 líneas, lenguaje sencillo, sin tecnicismos). 2. ACCIÓN: Una recomendación concreta que el paciente pueda hacer hoy (ej: tomar agua, evitar pantallas antes de dormir, hacer registro de síntomas). 3. PREGUNTA: Una pregunta de seguimiento simple para medir evolución (ej: '¿Cómo han estado tus dolores de cabeza esta semana?'). Si el paciente responde que sus síntomas empeoraron → fase_siguiente: F3 Si el paciente pregunta por consulta o paquete → fase_siguiente: F4 Si el paciente expresa angustia emocional intensa → fase_siguiente: HUMANO Adaptar el contenido de la tríada al programa clínico: Cefalea: hidratación, sueño, manejo de estrés, diario de migraña Epilepsia: adherencia, sueño regular, evitar triggers, no conducir Sueño: higiene del sueño, horarios, cafeína, pantallas Memoria: estimulación cognitiva, actividad física, socialización |
| --- |

5. Simulación del Proceso de Atención

A continuación se simula el flujo completo de atención de una paciente real desde el primer mensaje hasta la conclusión de Fase 4. Se muestra qué ocurre en Make y en Google Sheets en cada paso.

5.1 Datos de entrada del caso

| Campo | Valor |
| --- | --- |
| Paciente | María Torres |
| Teléfono WhatsApp | 573041234567 |
| Mensaje inicial | Hola buenas, me han recomendado este número. Tengo unos dolores de cabeza muy fuertes que no me dejan trabajar |
| Aseguramiento | Prepagada Sura |
| Ciudad | Medellín |
| Edad | 38 años |

5.2 Turno por turno — Simulación completa

|  | Turno 1  [Fase: F0 → F1] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Hola buenas, me han recomendado este número. Tengo unos dolores de cabeza muy fuertes que no me dejan trabajar |  |
| Agente: |  | ¡Hola! Bienvenida a ICN Salud. Soy NeurOrientador, tu asistente de orientación neurológica. Antes de comenzar, te informamos que tus datos serán tratados con confidencialidad según la Ley 1581 de 2012. ¿Me autorizas a continuar? 😊 |  |
| Make: |  | Make crea fila nueva en PACIENTES con telefono=573041234567, fase_actual=F1. Registra turno en CONVERSACIONES. |  |
| Sheets: |  | Nueva fila en PACIENTES. fase_actual=F1. historial_json=[{user:...},{assistant:...}] |  |

|  | Turno 2  [Fase: F1] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Sí, autorizo |  |
| Agente: |  | Perfecto, gracias María. Para orientarte mejor necesito algunos datos. ¿Cuál es tu nombre completo, tu edad y tu ciudad de residencia? |  |
| Make: |  | Make recupera paciente, llama a ChatGPT con prompt F1 + historial. Parsea respuesta JSON. |  |
| Sheets: |  | Sin cambios en PACIENTES aún. Nuevo turno en CONVERSACIONES. |  |

|  | Turno 3  [Fase: F1] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | María Torres, 38 años, vivo en Medellín |  |
| Agente: |  | Mucho gusto, María. ¿Tienes medicina prepagada, EPS o pagas de forma particular? |  |
| Make: |  | ChatGPT detecta nombre, edad, ciudad. campos_actualizar={nombre:'María Torres', edad:38, ciudad:'Medellín'}. Make actualiza PACIENTES. |  |
| Sheets: |  | PACIENTES: nombre=María Torres, edad=38, ciudad=Medellín |  |

|  | Turno 4  [Fase: F1 → F2] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Tengo prepagada Sura |  |
| Agente: |  | Perfecto. Atendemos varios programas neurológicos: Cefalea y migraña, Epilepsia, Trastornos del sueño, Memoria, Movimiento, entre otros. ¿El problema de los dolores de cabeza es lo principal que quieres consultar? |  |
| Make: |  | campos_actualizar={aseguramiento:'Prepagada', entidad_prepagada:'Sura', programa_clinico:'Cefalea', fase_actual:'F2'} |  |
| Sheets: |  | PACIENTES: aseguramiento=Prepagada, entidad_prepagada=Sura, programa_clinico=Cefalea, fase_actual=F2 |  |

|  | Turno 5  [Fase: F2 → F3] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Sí, principalmente eso, quiero entender qué me pasa |  |
| Agente: |  | Entendido. Voy a hacerte algunas preguntas sobre tus dolores para orientarte mejor. ¿El dolor es más bien pulsátil (como latidos) o es una presión constante? ¿Y en qué zona de la cabeza lo sientes principalmente? |  |
| Make: |  | campos_actualizar={motivo_contacto:'orientacion_clinica', fase_actual:'F3'}. Inicia árbol clínico. |  |
| Sheets: |  | PACIENTES: fase_actual=F3 |  |

|  | Turno 6  [Fase: F3 — D1, D2] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Es pulsátil, en el lado derecho. A veces me da náuseas también |  |
| Agente: |  | Gracias por contarme. ¿Cuántas veces a la semana te dan estos dolores aproximadamente? ¿Y desde hace cuánto tiempo tienes este problema? |  |
| Make: |  | Score D1=+2 (pulsátil unilateral), D2=+1 (náuseas). score_total=3. campos_actualizar={score_total:3} |  |
| Sheets: |  | PACIENTES: score_total=3 |  |

|  | Turno 7  [Fase: F3 — D3, D4] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Unas 3 o 4 veces a la semana, llevo como 3 meses así |  |
| Agente: |  | Eso es bastante frecuente y lo entiendo, debe ser muy difícil. Del 0 al 10, ¿qué tanto te afecta estos dolores en tu día a día — en el trabajo, en casa, en tus actividades normales? |  |
| Make: |  | Score D3=+3 (3+ veces/semana, 3 meses). score_total=6. campos_actualizar={score_total:6} |  |
| Sheets: |  | PACIENTES: score_total=6 |  |

|  | Turno 8  [Fase: F3 — D4, D5] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Un 7, hay días que no puedo ni trabajar |  |
| Agente: |  | Entiendo perfectamente. ¿Cuando tienes el dolor, eres sensible a la luz brillante o a los ruidos fuertes? |  |
| Make: |  | Score D4=+3 (7/10, afecta trabajo). score_total=9. campos_actualizar={score_total:9} |  |
| Sheets: |  | PACIENTES: score_total=9 |  |

|  | Turno 9  [Fase: F3 — D5, D6 → RESULTADO] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Sí, a los dos, tengo que cerrar las persianas y todo |  |
| Agente: |  | ¿Has tomado algún medicamento para estos dolores? ¿Te ha funcionado? |  |
| Make: |  | Score D5=+2 (luz y ruido). score_total=11. Pendiente D6. |  |
| Sheets: |  | PACIENTES: score_total=11 |  |

|  | Turno 10  [Fase: F3 → F4] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Solo ibuprofeno pero casi no me hace nada |  |
| Agente: |  | María, gracias por toda la información. Con base en lo que me contaste — la frecuencia, la intensidad, la sensibilidad a luz y ruido, y la poca respuesta al ibuprofeno — todo esto sugiere que podrías estar teniendo migraña de alta frecuencia, lo cual amerita evaluación con un neurólogo especialista. Te cuento que tenemos un paquete diagnóstico de Cefalea que incluye la consulta neurológica y los estudios de base. ¿Te gustaría que te cuente en qué consiste? |  |
| Make: |  | Score D6=+2. score_total=13. nivel_riesgo=Alto. fenotipo_probable='Migraña episódica frecuente'. fase_actual=F4. campos_actualizar={score_total:13, nivel_riesgo:'Alto', fenotipo_probable:'Migraña episódica frecuente', fase_actual:'F4'} |  |
| Sheets: |  | PACIENTES: score_total=13, nivel_riesgo=Alto, fenotipo_probable=Migraña episódica frecuente, fase_actual=F4 |  |

|  | Turno 11  [Fase: F4 — Objeción] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | ¿Y cuánto vale eso? |  |
| Agente: |  | El paquete diagnóstico de Cefalea tiene un valor de $XXX.000 e incluye: consulta con neurólogo especialista, valoración completa y plan de manejo. Considera que llevas 3 meses con dolores que te limitan el trabajo — una evaluación a tiempo evita que el problema avance y se vuelva más difícil de tratar. ¿Quieres que te dé más detalles o ya tienes alguna fecha en mente para agendar? |  |
| Make: |  | Detecta pregunta de precio como objeción. Maneja con argumento clínico-económico. fase_actual sigue F4. |  |
| Sheets: |  | Sin cambios. Conversación registrada. |  |

|  | Turno 12 — CONVERSIÓN  [Fase: F4 → F5] |  |  |
| --- | --- | --- | --- |
| Paciente: |  | Bueno, me convencí. ¿Cuándo tienen disponible? |  |
| Agente: |  | Qué buena decisión, María. Tenemos disponibilidad esta semana. ¿Te quedaría bien el jueves o el viernes? ¿Tienes preferencia de mañana o tarde? |  |
| Make: |  | Detecta intención de agendar. campos_actualizar={conversion:'Paquete diagnostico cefalea', fase_actual:'F5'}. Make notifica internamente al equipo para confirmar agenda. |  |
| Sheets: |  | PACIENTES: conversion=Paquete diagnostico cefalea, fase_actual=F5. Nueva fila en CITAS. |  |

5.3 Estado final en Google Sheets tras la simulación

| Campo | Valor final |
| --- | --- |
| paciente_id | PAC-20260320-001 |
| telefono | 573041234567 |
| nombre | María Torres |
| edad | 38 |
| ciudad | Medellín |
| aseguramiento | Prepagada |
| entidad_prepagada | Sura |
| fase_actual | F5 |
| programa_clinico | Cefalea |
| nivel_riesgo | Alto |
| score_total | 13 |
| fenotipo_probable | Migraña episódica frecuente |
| conversion | Paquete diagnóstico cefalea |
| fecha_cita | Por confirmar (jueves o viernes) |
| estado_cita | Pendiente |
| requiere_humano | FALSE |
| turnos_conversacion | 12 (registrados en hoja CONVERSACIONES) |
| notas_internas | Sin banderas rojas. Candidata a programa cefalea frecuente. |

6. Guía de Implementación — Pasos para poner en marcha el V1

6.1 Prerrequisitos

| Requisito | Detalle | Responsable |
| --- | --- | --- |
| Número WhatsApp verificado | Número de ICN Salud aprobado en Meta Business Manager | ICN / Meta |
| WhatsApp Business API activa | Configurada con proveedor directo (Meta Cloud API o BSP como 360dialog, Twilio) | Técnico |
| Cuenta Make | Plan Core o superior (para webhooks activos 24/7) | ICN |
| API Key de OpenAI | Cuenta con acceso a GPT-4o. Créditos suficientes para volumen esperado | ICN |
| Google Sheets configurado | Tres hojas creadas: PACIENTES, CONVERSACIONES, CITAS con columnas exactas de sección 2 | ICN / Técnico |

6.2 Orden de implementación recomendado para MVP

Crear el Google Sheets con las tres hojas y todos los campos de la sección 2. Agregar una fila de prueba en PACIENTES.

En Make, crear el Escenario 1. Agregar módulo Webhook → conectar con WhatsApp Business API. Verificar que los mensajes llegan.

Agregar módulo Google Sheets — Buscar fila y confirmar que detecta si el teléfono ya existe.

Agregar módulo ChatGPT con el prompt base más el prompt de F0. Probar con mensaje de texto libre.

Verificar que la respuesta JSON se parsea correctamente y los campos se escriben en Google Sheets.

Agregar módulo WhatsApp — Enviar mensaje para devolver la respuesta al paciente.

Implementar la lógica de router por fase (switch sobre campo fase_actual) para cambiar el prompt dinámicamente.

Agregar el Escenario 2 de recordatorios y probarlo con una cita de prueba.

Prueba completa del flujo: enviar mensajes manualmente simulando a María y verificar cada paso.

Activar en producción con el primer programa clínico: Cefalea. Monitorear durante 1 semana antes de agregar más programas.

6.3 Programas clínicos — Prioridad de implementación

| MVP — Implementar primero (mayor volumen esperado) |
| --- |
| 1. Cefalea / Migraña — prompts completos en esta documentación |
| 2. Neurodesarrollo — adaptar árbol D1-D6 para TDAH, autismo, retraso del desarrollo |
| 3. Trastornos del sueño — adaptar para insomnio, apnea, somnolencia |
| 4. Epilepsia — adaptar con énfasis en D2 (alarma de convulsión activa) |

| Fase 2 — Implementar después de validar MVP |
| --- |
| 5. Memoria y deterioro cognitivo |
| 6. ACV — requiere protocolo de alarma muy estricto en D2 |
| 7. Parálisis facial |
| 8. Movimiento / Parkinson |
| 9. Dolor neuropático / Neuropatías |
| 10. Neuromuscular / Desmielinizantes |

7. Puntos Críticos y Recomendaciones de Producción

| Riesgo | Descripción | Mitigación recomendada |
| --- | --- | --- |
| ChatGPT no responde JSON válido | Si la IA genera texto libre en lugar de JSON, Make falla al parsear | Agregar módulo de validación JSON en Make. Si falla, re-enviar con prompt de corrección. Máx 2 reintentos. |
| Historial JSON demasiado largo | Conversaciones largas elevan el costo por tokens y pueden exceder el límite de contexto | Mantener máximo 20 turnos en historial_json. Truncar los más antiguos. |
| Alarma clínica no detectada | La IA puede pasar por alto una bandera roja si el usuario no la describe claramente | Incluir en el prompt de F3 una lista explícita de palabras clave de alarma. Agregar filtro adicional en Make antes de chatGPT. |
| Duplicación de paciente | Si el usuario escribe desde otro número, se crea un registro nuevo sin historial | Por ahora aceptar como limitación del V1. En V2, agregar identificación por nombre + fecha nacimiento. |
| Costos API crecientes | Con alto volumen, el costo de GPT-4o puede crecer rápidamente | Monitorear tokens/mes. Si supera presupuesto, migrar F5 y F6 a mensajes estáticos y solo usar IA en F1-F4. |
| Make sin actividad (webhook timeout) | WhatsApp puede revocar webhooks inactivos o con muchos errores 5xx | Activar alertas de error en Make. Implementar respuesta fallback automática si la IA tarda >10s. |
| Datos sensibles en Sheets | Google Sheets no es HIPAA compliant por defecto | Para datos de salud sensibles, agregar control de acceso estricto. Evaluar migrar a Airtable o Supabase en V2. |

