# INSTRUCCIONES PARA INICIAR — NeurOrientador Python Agent

## Contexto global del agente de AI

Este repositorio contiene las especificaciones para implementar en Python el sistema **NeurOrientador + NeuroAsistente** de ICN Salud. Es un sistema clínico-comercial de teleorientación neurológica que opera por WhatsApp Business API + ManyChat, orquestado por Make (o equivalente Python), con Gemini como modelo de lenguaje y PostgreSQL como base de datos operativa.

**Reglas absolutas para todo el proyecto:**
- Nunca hardcodear secretos: usar variables de entorno para todos los tokens y URLs.
- La lógica crítica (scoring, alarmas, fases, SLA) vive en Python backend, NO en prompts de IA.
- El agente nunca diagnostica, formula medicamentos ni indica dosis.
- El servicio siempre se llama "teleorientación", no consulta médica.
- V6 es la versión canónica. Versiones anteriores complementan detalles que V6 no define.
- Toda salida de IA debe ser JSON válido en la estructura establecida.

---

## Orden de ejecución de specs (por dependencias)

```
FASE 1 — Infraestructura base (sin dependencias)
  spec_1  → config.py + schemas.py (Pydantic + env vars)
  spec_2  → db_repository.py + models.py (PostgreSQL ORM + CRUD)
  spec_3  → alarm_filter.py (detección pre-IA)

FASE 2 — Core de la conversación (requiere Fase 1)
  spec_4  → llm_client.py + json_guard.py (cliente Gemini/OpenAI + validación JSON)
  spec_5  → scoring.py (cálculo D1-D6, nivel_riesgo, flag_alarma)
  spec_6  → phase_router.py + prompts/ (transición de fases F0-F4)

FASE 3 — Canales y escalamiento (requiere Fase 2)
  spec_7  → whatsapp_client.py + manychat_client.py
  spec_8  → escalation_service.py + SLA

FASE 4 — NeuroAsistente y Neuroasesor (requiere Fase 3)
  spec_9  → neuroasistente_service.py (acompañamiento post-agenda)
  spec_10 → neuroasesor_service.py + daily_reports.py

FASE 5 — Auditoría y calidad (requiere Fase 4)
  spec_11 → audit_log.py (trazabilidad completa)
  spec_12 → tests/ (pruebas unitarias obligatorias)
```

---

## Cómo ejecutar el primer prompt en Claude Code

1. Abre Claude Code en la raíz del repositorio Python del proyecto.
2. Carga el archivo `CODEX_CONTEXT_NEURORIENTADOR_ICN.md` como contexto base con:
   ```
   /context add CODEX_CONTEXT_NEURORIENTADOR_ICN.md
   ```
3. Ejecuta spec_1 pegando el contenido de `spec/spec_1/prompt.md` en Claude Code.
4. Valida que los archivos `config.py` y `schemas.py` se generaron correctamente antes de avanzar a spec_2.

---

## Archivos de entrada requeridos para el primer prompt

| Spec   | Archivo/Input requerido                         |
|--------|-------------------------------------------------|
| spec_1 | Ninguno (arranque desde cero)                   |
| spec_2 | `config.py` generado en spec_1                  |
| spec_3 | `config.py` y `schemas.py` de spec_1            |
| spec_4 | specs 1-2 completas                             |
| spec_5 | `schemas.py` de spec_1                          |
| spec_6 | specs 1-5 completas + carpeta `prompts/`        |
| spec_7 | specs 1-4 completas                             |
| spec_8 | specs 1-7 completas                             |
| spec_9 | specs 1-8 completas                             |
| spec_10| specs 1-9 completas                             |
| spec_11| specs 1-10 completas                            |
| spec_12| Todas las specs anteriores completas            |

---

## Variables de entorno requeridas (nunca hardcodear)

```env
# IA
GEMINI_API_KEY=
OPENAI_API_KEY=          # alternativa si no se usa Gemini

# WhatsApp Business API
WHATSAPP_TOKEN=
WHATSAPP_PHONE_ID=
WHATSAPP_WEBHOOK_SECRET=  # para verificación HMAC

# ManyChat
MANYCHAT_API_TOKEN=

# PostgreSQL
DATABASE_URL=postgresql://user:password@host:5432/neurorientador

# ICN interno
ICN_NEUROASESOR_WHATSAPP=     # número interno para escalamientos
ICN_COORDINADOR_WHATSAPP=     # para alertas de SLA incumplido

# Make (si se usa webhook)
MAKE_WEBHOOK_URL=

# Timezone
TZ=America/Bogota
```
