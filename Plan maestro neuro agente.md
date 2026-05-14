# PLAN MAESTRO — NeurOrientador + NeuroAsistente ICN Salud
> Stack: Python · FastAPI · Docker · PostgreSQL · Twilio · Multi-LLM (Claude / OpenAI / Gemini)  
> Deploy de prueba: Railway  
> Versión de referencia: V6 del CLAUDE CODE_CONTEXT

---

## 0. Qué vas a construir (resumen ejecutivo)

Un agente de IA de teleorientación neurológica que:
- Recibe mensajes de WhatsApp de pacientes vía Twilio (sandbox para pruebas)
- Los guía por 5 fases clínicas (F0→F4) más un módulo de acompañamiento (NeuroAsistente)
- Calcula un score de riesgo neurológico (D1–D6) y clasifica nivel de riesgo
- Almacena todo en PostgreSQL (pacientes, conversaciones, citas, trazabilidad)
- Puede usar Claude, OpenAI o Gemini como motor de IA (configurable por variable de entorno)
- Escala conversaciones críticas al Neuroasesor humano
- Nunca diagnostica ni formula medicamentos — solo teleorienta

---

## 1. Estructura de carpetas del proyecto

```
neuro-agente/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Entrada FastAPI, registro de routers
│   ├── config.py                # Carga todas las variables de entorno
│   ├── database.py              # Conexión SQLAlchemy + pool PostgreSQL
│   │
│   ├── routers/
│   │   ├── webhook.py           # POST /webhook/twilio  ← punto de entrada Twilio
│   │   ├── health.py            # GET /health           ← Railway health check
│   │   └── admin.py             # GET /admin/patients   ← consulta interna (opcional)
│   │
│   ├── models/
│   │   ├── patient.py           # Tabla PACIENTES
│   │   ├── conversation.py      # Tabla CONVERSACIONES (cada turno)
│   │   ├── appointment.py       # Tabla CITAS
│   │   └── trace.py             # Tabla TRAZABILIDAD (auditoría)
│   │
│   ├── schemas/
│   │   ├── patient.py           # Pydantic: PatientCreate, PatientOut
│   │   ├── conversation.py      # Pydantic: TurnCreate, TurnOut
│   │   └── agent_response.py    # Pydantic: estructura JSON que devuelve el LLM
│   │
│   ├── services/
│   │   ├── alarm_filter.py      # Detección de palabras clave críticas ANTES del LLM
│   │   ├── phase_router.py      # Decide qué fase corresponde y carga el prompt correcto
│   │   ├── score_engine.py      # Calcula score_total y nivel_riesgo (D1–D6)
│   │   ├── llm_router.py        # Elige Claude / OpenAI / Gemini según env var
│   │   ├── llm_claude.py        # Llamada a Anthropic API
│   │   ├── llm_openai.py        # Llamada a OpenAI API
│   │   ├── llm_gemini.py        # Llamada a Google Gemini API
│   │   ├── json_validator.py    # Valida y reintenta si el LLM no devuelve JSON
│   │   ├── escalation.py        # Lógica de escalamiento humano + SLA 15 min
│   │   └── twilio_sender.py     # Envía mensajes de vuelta por Twilio/WhatsApp
│   │
│   ├── prompts/
│   │   ├── base_system.py       # System prompt base (tono triádico, reglas legales)
│   │   ├── f0_intencion.py      # Prompt F0: clasificación de intención
│   │   ├── f1_consentimiento.py # Prompt F1: consentimiento + identificación
│   │   ├── f2_problema.py       # Prompt F2: selección de problema neurológico
│   │   ├── f3_cefalea.py        # Prompt F3: árbol clínico Cefalea (D1–D6)
│   │   ├── f3_sueno.py          # Prompt F3: árbol Trastornos del sueño
│   │   ├── f3_neurodesarrollo.py# Prompt F3: árbol Neurodesarrollo
│   │   ├── f3_epilepsia.py      # Prompt F3: árbol Epilepsia
│   │   ├── f4_conversion.py     # Prompt F4: conversión a cita
│   │   └── neuroasistente.py    # Prompt post-agenda: recordatorios y acompañamiento
│   │
│   └── utils/
│       ├── twilio_signature.py  # Verificación de firma de Twilio (seguridad)
│       └── history_manager.py   # Mantiene historial máx 20 turnos
│
├── migrations/
│   └── init.sql                 # SQL inicial: crea las 4 tablas con todos los campos
│
├── tests/
│   ├── test_alarm_filter.py
│   ├── test_score_engine.py
│   ├── test_phase_router.py
│   └── test_webhook.py          # Simula mensajes de Twilio
│
├── .env.example                 # Plantilla con TODAS las variables (sin valores reales)
├── .env                         # Tu archivo real (en .gitignore)
├── .gitignore
├── Dockerfile
├── docker-compose.yml           # App + PostgreSQL para desarrollo local
├── requirements.txt
└── README.md
```

---

## 2. Variables de entorno (`.env.example`)

Copia este archivo como `.env` y llena los valores. El proyecto no funcionará sin estas variables.

```env
# ─── BASE DE DATOS ─────────────────────────────────────────────
DATABASE_URL=postgresql://usuario:password@db:5432/neuro_agente
# En Railway se reemplaza automáticamente por la URL interna de Postgres

# ─── TWILIO ────────────────────────────────────────────────────
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
# El número de sandbox de Twilio para pruebas es +14155238886
# En producción: tu número aprobado de WhatsApp Business

# ─── MOTOR DE IA (elige uno como primario) ─────────────────────
LLM_PROVIDER=claude
# Opciones: claude | openai | gemini

ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ─── CONFIGURACIÓN DEL AGENTE ──────────────────────────────────
LLM_MODEL_CLAUDE=claude-sonnet-4-20250514
LLM_MODEL_OPENAI=gpt-4o
LLM_MODEL_GEMINI=gemini-1.5-pro
MAX_HISTORY_TURNS=20
MAX_JSON_RETRIES=2

# ─── ESCALAMIENTO HUMANO ───────────────────────────────────────
ESCALATION_PHONE=whatsapp:+57XXXXXXXXXX
# Número del Neuroasesor que recibirá las alertas por WhatsApp
ESCALATION_SLA_MINUTES=15

# ─── SEGURIDAD ─────────────────────────────────────────────────
SECRET_KEY=cambia_esto_por_una_cadena_aleatoria_larga
VALIDATE_TWILIO_SIGNATURE=true
# En pruebas locales puedes poner false, en producción siempre true

# ─── RAILWAY / DEPLOY ──────────────────────────────────────────
PORT=8000
ENVIRONMENT=development
# Opciones: development | production
```

---

## 3. Esquema de base de datos (PostgreSQL)

### Tabla PACIENTES
```sql
CREATE TABLE pacientes (
    id                  SERIAL PRIMARY KEY,
    paciente_id         VARCHAR(30) UNIQUE NOT NULL,  -- PAC-YYYYMMDD-NNN
    telefono            VARCHAR(20) UNIQUE NOT NULL,
    nombre              VARCHAR(100),
    edad                INTEGER,
    ciudad              VARCHAR(100),
    aseguramiento       VARCHAR(50),    -- EPS | Prepagada | Particular
    entidad             VARCHAR(100),
    fase_actual         VARCHAR(10) DEFAULT 'F0',
    programa_clinico    VARCHAR(50),
    score_total         INTEGER DEFAULT 0,
    nivel_riesgo        VARCHAR(20),    -- Bajo | Medio | Alto | Alarma
    fenotipo_probable   VARCHAR(200),
    motivo_contacto     VARCHAR(100),
    conversion          VARCHAR(200),
    requiere_humano     BOOLEAN DEFAULT FALSE,
    flag_alarma         BOOLEAN DEFAULT FALSE,
    consentimiento      BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);
```

### Tabla CONVERSACIONES
```sql
CREATE TABLE conversaciones (
    id              SERIAL PRIMARY KEY,
    paciente_id     VARCHAR(30) REFERENCES pacientes(paciente_id),
    turno           INTEGER NOT NULL,
    fase            VARCHAR(10),
    rol             VARCHAR(20),  -- paciente | agente | sistema
    mensaje         TEXT NOT NULL,
    llm_provider    VARCHAR(20),  -- claude | openai | gemini
    tokens_usados   INTEGER,
    latencia_ms     INTEGER,
    json_valido     BOOLEAN,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### Tabla CITAS
```sql
CREATE TABLE citas (
    id              SERIAL PRIMARY KEY,
    paciente_id     VARCHAR(30) REFERENCES pacientes(paciente_id),
    programa        VARCHAR(50),
    tipo_cita       VARCHAR(100),
    fecha_propuesta VARCHAR(100),
    estado          VARCHAR(30) DEFAULT 'pendiente',
    notas           TEXT,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### Tabla TRAZABILIDAD
```sql
CREATE TABLE trazabilidad (
    id              SERIAL PRIMARY KEY,
    paciente_id     VARCHAR(30),
    evento          VARCHAR(100),  -- fase_cambio | alarma | escalamiento | json_retry
    detalle         TEXT,
    valor_anterior  VARCHAR(200),
    valor_nuevo     VARCHAR(200),
    created_at      TIMESTAMP DEFAULT NOW()
);
```

---

## 4. Estructura del JSON que produce el LLM

El LLM **siempre** debe devolver este JSON. El backend lo valida, nunca confía en texto libre.

```json
{
  "respuesta_visible": "Texto que verá el paciente por WhatsApp",
  "campos_actualizar": {
    "fase_actual": "F3",
    "programa_clinico": "Cefalea",
    "score_total": 6,
    "nivel_riesgo": null,
    "fenotipo_probable": null,
    "motivo_contacto": "orientacion_clinica",
    "nombre": null,
    "edad": null,
    "ciudad": null,
    "aseguramiento": null,
    "entidad": null,
    "consentimiento": false
  },
  "flag_alarma": false,
  "requiere_humano": false,
  "razon_escalamiento": null,
  "notas_internas": "Nota para el Neuroasesor, no visible al paciente"
}
```

---

## 5. Lógica crítica del backend (nunca delegar al LLM)

Estas validaciones van en Python **antes y después** de llamar al LLM:

### Filtro de alarmas (ANTES del LLM)
Palabras que activan `flag_alarma = TRUE` e inmediato escalamiento:
- Convulsión activa, convulsionando ahora
- Pérdida de conciencia
- Parálisis súbita, caída de la cara
- Dificultad para hablar de repente
- Peor dolor de cabeza de mi vida, trueno
- Pensamientos de hacerme daño, suicidio

### Score engine (independiente del LLM)
```
D1: Características del dolor/síntoma      → 0 a +3
D2: Síntomas asociados / señales de alarma → 0 a +3 (o ALARMA directa)
D3: Frecuencia y duración                  → 0 a +3
D4: Impacto funcional                      → 0 a +3
D5: Factores agravantes/atenuantes         → 0 a +2
D6: Respuesta a tratamiento previo         → 0 a +2

nivel_riesgo:
  0-4  → Bajo
  5-8  → Medio
  9-13 → Alto
  D2 con alarma → Alarma (independiente del score)
```

### Validación JSON (reintentos)
1. El LLM responde → parsear JSON
2. Si falla → reenviar con mensaje: "Tu respuesta anterior no era JSON válido. Responde ÚNICAMENTE con el JSON en el formato indicado."
3. Máximo 2 reintentos → si falla → respuesta fallback genérica + trazar el error

### Historial de conversación
- Máximo 20 turnos en memoria
- Los más antiguos se truncan
- El historial completo queda en PostgreSQL

---

## 6. Flujo de una conversación (paso a paso técnico)

```
1. Paciente envía mensaje por WhatsApp
2. Twilio recibe y hace POST a /webhook/twilio
3. FastAPI valida firma de Twilio (seguridad)
4. Se busca el teléfono en PACIENTES
   → Si no existe: crear registro con fase_actual=F0
   → Si existe: cargar registro y historial (últimos 20 turnos)
5. alarm_filter.py escanea el mensaje ANTES del LLM
   → Si hay alarma: flag_alarma=TRUE, escalar, enviar respuesta de emergencia
6. phase_router.py determina la fase actual y carga el prompt correcto
7. score_engine.py prepara los datos de scoring acumulados
8. llm_router.py envía al proveedor configurado (Claude / OpenAI / Gemini)
9. json_validator.py valida la respuesta (hasta 2 reintentos)
10. Los campos_actualizar se aplican a la tabla PACIENTES
11. El turno se registra en CONVERSACIONES
12. Si requiere_humano=TRUE → escalation.py notifica al Neuroasesor
13. twilio_sender.py envía respuesta_visible al paciente
14. trazabilidad registra todos los eventos importantes
```

---

## 7. Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 8. docker-compose.yml (desarrollo local)

```yaml
version: "3.9"

services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: usuario
      POSTGRES_PASSWORD: password
      POSTGRES_DB: neuro_agente
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./migrations/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U usuario -d neuro_agente"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

---

## 9. requirements.txt

```
fastapi==0.115.0
uvicorn[standard]==0.30.6
sqlalchemy==2.0.35
psycopg2-binary==2.9.9
pydantic==2.9.2
pydantic-settings==2.5.2
python-dotenv==1.0.1
twilio==9.3.0
anthropic==0.35.0
openai==1.51.0
google-generativeai==0.8.2
httpx==0.27.2
pytest==8.3.3
pytest-asyncio==0.24.0
```

---

## 10. Deploy en Railway (paso a paso)

### Preparación antes de subir
1. Crear repositorio en GitHub (privado)
2. Asegurarte de que `.env` está en `.gitignore`
3. Subir todo el código

### En Railway
1. Ir a [railway.app](https://railway.app) → New Project
2. Deploy from GitHub repo → seleccionar tu repo
3. Add Plugin → PostgreSQL (Railway crea la base de datos automáticamente)
4. En Variables → agregar todas las variables de tu `.env.example` con los valores reales
5. La variable `DATABASE_URL` Railway la inyecta sola si usas su Postgres plugin
6. Railway detecta el Dockerfile automáticamente
7. El deploy tarda ~2 minutos → obtienes una URL pública tipo `https://tu-app.up.railway.app`

### Configurar Twilio para recibir mensajes
1. En Twilio Console → Messaging → Sandbox for WhatsApp
2. En "When a message comes in" poner: `https://tu-app.up.railway.app/webhook/twilio`
3. En tu WhatsApp personal: enviar `join <tu-palabra-sandbox>` al número de Twilio
4. Listo para probar

---

## 11. Orden de construcción recomendado

Construye en este orden exacto. No adelantes fases.

```
FASE 1 — Cimientos (sin IA todavía)
  □ Estructura de carpetas
  □ config.py con todas las variables de entorno
  □ database.py con SQLAlchemy
  □ migrations/init.sql con las 4 tablas
  □ models/ (Patient, Conversation, Appointment, Trace)
  □ docker-compose.yml funcional
  □ GET /health funcionando
  □ Verificar conexión a PostgreSQL

FASE 2 — Webhook básico
  □ POST /webhook/twilio recibe el mensaje de Twilio
  □ Verifica firma de Twilio
  □ Crea o carga el registro del paciente
  □ Responde "Hola" de vuelta (sin IA aún)
  □ Probar con Twilio sandbox desde tu WhatsApp

FASE 3 — LLM Router
  □ llm_claude.py con llamada básica
  □ llm_openai.py con llamada básica
  □ llm_gemini.py con llamada básica
  □ llm_router.py que elige según LLM_PROVIDER
  □ Prueba que los 3 responden correctamente

FASE 4 — Prompts y JSON
  □ base_system.py con el system prompt (tono triádico + reglas legales)
  □ Prompts F0 y F1 primero
  □ json_validator.py con reintentos
  □ Verificar que el JSON se parsea bien
  □ Los campos_actualizar se escriben en PostgreSQL

FASE 5 — Fases clínicas
  □ phase_router.py (switch sobre fase_actual)
  □ Prompts F2, F3 (Cefalea primero), F4
  □ score_engine.py (D1–D6 + nivel_riesgo)
  □ Probar flujo completo F0→F4 simulando a "María"

FASE 6 — Seguridad clínica
  □ alarm_filter.py con palabras clave críticas
  □ escalation.py (notificación al Neuroasesor)
  □ history_manager.py (máx 20 turnos)
  □ Trazabilidad en cada evento importante

FASE 7 — NeuroAsistente
  □ Prompts post-agenda
  □ Recordatorios de cita
  □ Seguimiento posterior

FASE 8 — Pruebas y deploy
  □ Tests unitarios (alarm_filter, score_engine, phase_router)
  □ Test de integración del webhook completo
  □ Deploy en Railway
  □ Prueba real desde WhatsApp
  □ Monitorear 1 semana con programa Cefalea antes de agregar más
```

---

## 12. Prompt maestro para construir el proyecto con IA

Cuando vayas a pedirle a Claude Code (o cualquier agente de código) que construya el proyecto, usa exactamente este prompt. Pégalo completo junto con el archivo CLAUDE CODE_CONTEXT_NEURORIENTADOR_ICN.md:

---

```
Eres un desarrollador Python senior. Vas a construir desde cero el sistema NeurOrientador + NeuroAsistente para ICN Salud siguiendo el PLAN_MAESTRO y el CLAUDE CODE_CONTEXT adjuntos.

REGLAS ABSOLUTAS:
1. Implementa SOLO la FASE 1 del plan maestro ahora. Espera confirmación antes de continuar.
2. Nunca inventes funcionalidades no descritas en el CLAUDE CODE_CONTEXT.
3. Nunca hardcodees secretos. Todo va en variables de entorno cargadas desde config.py.
4. La lógica crítica (alarm_filter, score_engine, json_validator, escalamiento) va en Python, nunca solo en prompts.
5. Toda respuesta del LLM debe ser JSON validado antes de usarse.
6. El agente nunca diagnostica ni formula medicamentos. Solo teleorienta.
7. F3 siempre antes de agendar.
8. Usa el esquema de tablas exacto del plan maestro.
9. Escribe docstrings en cada función y módulo.
10. Genera tests para alarm_filter.py y score_engine.py.

STACK:
- Python 3.12 + FastAPI + SQLAlchemy + PostgreSQL
- Twilio para WhatsApp
- Multi-LLM: Claude (primario), OpenAI, Gemini (fallback)
- Docker + docker-compose para desarrollo
- Deploy en Railway

EMPIEZA por la FASE 1: estructura de carpetas, config.py, database.py, models/, migrations/init.sql y docker-compose.yml. Cuando termines la Fase 1 dime "Fase 1 completada" y espera.
```

---

## 13. Puntos críticos a no olvidar

| Riesgo | Qué hacer |
|--------|-----------|
| LLM no devuelve JSON válido | `json_validator.py` con 2 reintentos automáticos |
| Historial muy largo (tokens y costo) | Máximo 20 turnos en contexto |
| Alarma clínica no detectada | `alarm_filter.py` corre ANTES del LLM, no después |
| Datos sensibles de salud | PostgreSQL con contraseña fuerte, no exponer DB directamente |
| Costo de API creciente | Monitorear tokens/mes. Configurar LLM_PROVIDER a modelo más económico si sube |
| Paciente desde otro número | Limitación del V1: se crea registro nuevo. Documentarlo. |
| Webhook sin autenticación | Siempre validar firma de Twilio (`VALIDATE_TWILIO_SIGNATURE=true`) |

---

## 14. Checklist antes de ir a producción

- [ ] Variables de entorno configuradas en Railway (nunca en código)
- [ ] `VALIDATE_TWILIO_SIGNATURE=true` en producción
- [ ] Número de WhatsApp Business aprobado en Meta (no sandbox)
- [ ] PostgreSQL con backups automáticos activados en Railway
- [ ] Logs de trazabilidad funcionando para cada conversación
- [ ] Prueba completa del flujo F0→F4 con datos reales de Cefalea
- [ ] Número del Neuroasesor configurado en `ESCALATION_PHONE`
- [ ] Revisión legal del lenguaje del agente (sin diagnósticos)
- [ ] Monitoreo de costos de API activo

---

*Generado con base en CLAUDE CODE_CONTEXT_NEURORIENTADOR_ICN.md V6 — ICN Salud*