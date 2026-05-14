# Prompt — Spec 2: supabase_repository.py + migrations/

Eres un Ingeniero de Backend Python experto en PostgreSQL y Supabase. Tu tarea es implementar el repositorio de persistencia para el sistema NeurOrientador de ICN Salud usando Supabase como base de datos.

## Contexto
El sistema persiste todos sus datos en PostgreSQL a través de Supabase. El cliente Python es `supabase-py` (`from supabase import create_client`). La clave primaria de `pacientes` es el número de teléfono WhatsApp. El campo `historial_json` es JSONB nativo — sin serialización manual. Los archivos `config.py` y `schemas.py` ya existen (Spec 1).

## Entrega requerida

### Parte 1: `migrations/001_initial_schema.sql`
DDL completo para ejecutar en el SQL Editor de Supabase. Incluir:

**ENUMs:**
```sql
CREATE TYPE fase_enum AS ENUM ('F0','F1','F2','F3','F4','ADMIN','HUMANO');
CREATE TYPE nivel_riesgo_enum AS ENUM ('Bajo','Moderado','Alto','Alarma');
CREATE TYPE prioridad_enum AS ENUM ('agendado','particular','general');
CREATE TYPE tipo_escalamiento_enum AS ENUM ('alarma_critica','clinico','comercial','solicitud_paciente','error_sistema','neuroasistente_clinico','neuroasistente_comercial');
CREATE TYPE estado_interaccion_enum AS ENUM ('enviado','respondido','pendiente','cerrado','escalado');
```

**Tabla `pacientes`** (clave primaria: telefono):
```sql
CREATE TABLE pacientes (
    telefono TEXT PRIMARY KEY,
    paciente_id TEXT UNIQUE NOT NULL,
    nombre TEXT,
    edad INTEGER,
    ciudad TEXT,
    aseguramiento TEXT,
    entidad_prepagada TEXT,
    consentimiento_datos_clinicos BOOLEAN DEFAULT FALSE,
    consentimiento_teleorientacion BOOLEAN DEFAULT FALSE,
    consentimiento_investigacion BOOLEAN DEFAULT FALSE,
    timestamp_consentimiento TIMESTAMPTZ,
    fase_actual fase_enum DEFAULT 'F0',
    tipo_consulta TEXT,
    programa_clinico TEXT,
    problema_seleccionado INTEGER,
    guia_soporte TEXT,
    cie10 TEXT,
    nivel_riesgo nivel_riesgo_enum,
    score_total INTEGER DEFAULT 0,
    fenotipo_probable TEXT,
    respuestas_orientacion JSONB,
    reporte_enviado BOOLEAN DEFAULT FALSE,
    conversion TEXT,
    fecha_cita DATE,
    canal_agenda TEXT,
    estado_cita TEXT,
    fecha_primera_orientacion DATE,
    fecha_ultima_orientacion DATE,
    cohorte TEXT,
    requiere_humano BOOLEAN DEFAULT FALSE,
    requiere_revision_medica BOOLEAN DEFAULT FALSE,
    motivo_escalamiento TEXT,
    error_json BOOLEAN DEFAULT FALSE,
    error_operativo TEXT,
    version_prompt TEXT,
    version_flujo TEXT DEFAULT 'v6.0',
    historial_json JSONB DEFAULT '[]',
    notas_internas TEXT,
    prioridad_operativa prioridad_enum DEFAULT 'general',
    fecha_creacion TIMESTAMPTZ DEFAULT NOW(),
    ultima_actividad TIMESTAMPTZ DEFAULT NOW()
);
```

**Tablas restantes:** `conversaciones`, `citas`, `escalamientos`, `neuroasistente_interacciones`, `neuroasesor_interacciones`, `resumenes_diarios`, `cohortes_investigacion` con sus campos, FKs y tipos correspondientes al modelo de datos V6.

**Índices:**
```sql
CREATE INDEX idx_conversaciones_paciente ON conversaciones(paciente_id);
CREATE INDEX idx_escalamientos_paciente ON escalamientos(paciente_id, timestamp_escalamiento);
CREATE INDEX idx_na_interacciones_paciente ON neuroasistente_interacciones(paciente_id, estado_interaccion);
CREATE INDEX idx_na_interacciones_fecha ON neuroasistente_interacciones(fecha_hora);
```

### Parte 2: `supabase_repository.py`
```python
from supabase import create_client, Client
import config

class SupabaseRepository:
    def __init__(self):
        self.client: Client = create_client(
            config.SUPABASE_URL, 
            config.SUPABASE_SERVICE_KEY
        )
```

**Métodos de `pacientes`:**
```python
def get_paciente_by_telefono(self, telefono: str) -> Optional[Paciente]
def create_paciente(self, paciente: Paciente) -> Paciente
def update_paciente(self, telefono: str, campos: dict) -> None
    # Siempre incluir ultima_actividad en campos al hacer update
```

**Métodos de `conversaciones`:**
```python
def insert_conversacion(self, conv: Conversacion) -> None
```

**Métodos de `citas`:**
```python
def insert_cita(self, cita: Cita) -> None
def update_cita(self, cita_id: str, campos: dict) -> None
def get_citas_pendientes_seguimiento(self) -> List[Cita]
    # WHERE fecha_cita = CURRENT_DATE - 1 AND seguimiento_post = FALSE AND confirmacion = 'Confirmada'
```

**Métodos de `escalamientos`:**
```python
def insert_escalamiento(self, esc: Escalamiento) -> None
def update_escalamiento(self, escalamiento_id: str, campos: dict) -> None
def get_escalamientos_sin_respuesta(self) -> List[Escalamiento]
    # WHERE timestamp_respuesta_humano IS NULL
```

**Métodos de `neuroasistente_interacciones`:**
```python
def insert_neuroasistente_interaccion(self, i: NeuroAsistenteInteraccion) -> None
def update_neuroasistente_interaccion(self, interaccion_id: str, campos: dict) -> None
def get_interacciones_del_dia(self, fecha: date) -> List[NeuroAsistenteInteraccion]
def get_interaccion_activa_por_paciente(self, paciente_id: str, cita_id: str) -> Optional[NeuroAsistenteInteraccion]
    # WHERE paciente_id=... AND cita_id=... AND estado_interaccion='enviado' ORDER BY fecha_hora DESC LIMIT 1
```

**Métodos de `neuroasesor_interacciones` y `resumenes_diarios`:**
```python
def insert_neuroasesor_interaccion(self, i: NeuroAsesorInteraccion) -> None
def insert_resumen_diario(self, r: ResumenDiario) -> None
```

**Método de `cohortes_investigacion`:**
```python
def insert_cohorte_investigacion(self, paciente: Paciente) -> None
    # CRÍTICO: verificar consentimiento_investigacion == True antes de insertar
    # Solo insertar campos anonimizados: sin telefono, sin nombre
```

## Manejo de errores
- Capturar `postgrest.exceptions.APIError` con retry (máx 3, backoff 2s exponencial)
- `get_paciente_by_telefono`: si Supabase retorna error "PGRST116" (no rows) → retornar None, no lanzar excepción

## Ventajas clave vs Sheets
- `historial_json` es JSONB nativo → no se serializa/deserializa manualmente, se trabaja directamente como lista Python
- Queries con filtros reales (`.eq()`, `.gte()`, `.lt()`) en lugar de iterar filas
- Timestamps con timezone incluidos en el tipo `TIMESTAMPTZ`

## Actualizar `requirements.txt`
Reemplazar `gspread` y `google-auth` por:
```
supabase>=2.0.0
```
