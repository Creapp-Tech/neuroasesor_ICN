-- Migración inicial para Supabase
-- Ejecutar en el SQL Editor de Supabase

-- ENUMs
CREATE TYPE fase_enum AS ENUM ('F0','F1','F2','F3','F4','ADMIN','HUMANO');
CREATE TYPE nivel_riesgo_enum AS ENUM ('Bajo','Moderado','Alto','Alarma');
CREATE TYPE prioridad_enum AS ENUM ('agendado','particular','general');
CREATE TYPE tipo_escalamiento_enum AS ENUM ('alarma_critica','clinico','comercial','solicitud_paciente','error_sistema','neuroasistente_clinico','neuroasistente_comercial');
CREATE TYPE estado_interaccion_enum AS ENUM ('enviado','respondido','pendiente','cerrado','escalado');
CREATE TYPE resultado_neuroasesor_enum AS ENUM ('cerrado','pendiente','escalado_medico','nueva_cita_agendada','rechazo','sin_respuesta');
CREATE TYPE responsable_enum AS ENUM ('NeuroAsistente_automatico','Neuroasesor_humano','Sistema_Make');

-- Tabla pacientes
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
    respuestas_orientacion JSONB DEFAULT '{}',
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

-- Tabla conversaciones
CREATE TABLE conversaciones (
    conv_id TEXT PRIMARY KEY,
    paciente_id TEXT REFERENCES pacientes(paciente_id),
    telefono TEXT REFERENCES pacientes(telefono),
    fase TEXT,
    mensaje_usuario TEXT,
    respuesta_agente TEXT,
    guia_soporte_turno TEXT,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    tokens_usados INTEGER DEFAULT 0,
    flag_alarma BOOLEAN DEFAULT FALSE,
    escalado_humano BOOLEAN DEFAULT FALSE,
    version_prompt TEXT
);

-- Tabla citas
CREATE TABLE citas (
    cita_id TEXT PRIMARY KEY,
    paciente_id TEXT REFERENCES pacientes(paciente_id),
    tipo TEXT,
    programa TEXT,
    fecha_cita DATE,
    hora_cita TEXT,
    canal_agenda TEXT,
    confirmacion TEXT,
    seguimiento_post BOOLEAN DEFAULT FALSE,
    resultado_post TEXT
);

-- Tabla escalamientos
CREATE TABLE escalamientos (
    escalamiento_id TEXT PRIMARY KEY,
    paciente_id TEXT REFERENCES pacientes(paciente_id),
    timestamp_escalamiento TIMESTAMPTZ DEFAULT NOW(),
    timestamp_respuesta_humano TIMESTAMPTZ,
    tiempo_respuesta_humano FLOAT,
    cumple_sla_15min BOOLEAN,
    tipo_escalamiento tipo_escalamiento_enum,
    prioridad_paciente prioridad_enum,
    fase_origen TEXT,
    motivo TEXT,
    resolucion TEXT,
    responsable TEXT,
    resultado TEXT
);

-- Tabla neuroasistente_interacciones
CREATE TABLE neuroasistente_interacciones (
    interaccion_id TEXT PRIMARY KEY,
    paciente_id TEXT REFERENCES pacientes(paciente_id),
    cita_id TEXT REFERENCES citas(cita_id),
    fecha_hora TIMESTAMPTZ DEFAULT NOW(),
    canal_contacto TEXT,
    tipo_interaccion TEXT,
    mensaje_enviado TEXT,
    respuesta_paciente TEXT,
    estado_interaccion estado_interaccion_enum DEFAULT 'enviado',
    requiere_revision_clinica BOOLEAN DEFAULT FALSE,
    requiere_revision_comercial BOOLEAN DEFAULT FALSE,
    notas_internas TEXT,
    responsable responsable_enum,
    accion_generada TEXT,
    prioridad_paciente prioridad_enum,
    version_flujo TEXT,
    timestamp_actualizacion TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla neuroasesor_interacciones
CREATE TABLE neuroasesor_interacciones (
    neuroasesor_interaccion_id TEXT PRIMARY KEY,
    paciente_id TEXT REFERENCES pacientes(paciente_id),
    fecha_hora_inicio TIMESTAMPTZ DEFAULT NOW(),
    fecha_hora_fin TIMESTAMPTZ,
    tiempo_respuesta_humano FLOAT,
    cumple_sla_15min BOOLEAN,
    canal TEXT,
    tipo_interaccion TEXT,
    prioridad_paciente prioridad_enum,
    resumen_conversacion TEXT,
    resultado resultado_neuroasesor_enum,
    oportunidad_detectada TEXT,
    incidencia TEXT,
    notas_internas TEXT,
    responsable TEXT,
    version_flujo TEXT
);

-- Tabla resumenes_diarios
CREATE TABLE resumenes_diarios (
    resumen_id TEXT PRIMARY KEY,
    fecha DATE UNIQUE NOT NULL,
    total_interacciones_na INTEGER DEFAULT 0,
    total_respondidas INTEGER DEFAULT 0,
    total_sin_respuesta INTEGER DEFAULT 0,
    casos_revision_clinica INTEGER DEFAULT 0,
    casos_revision_comercial INTEGER DEFAULT 0,
    total_escalamientos INTEGER DEFAULT 0,
    sla_cumplido_pct FLOAT DEFAULT 0.0,
    tiempo_respuesta_promedio FLOAT DEFAULT 0.0,
    total_interacciones_neuroasesor INTEGER DEFAULT 0,
    resumen_narrativo TEXT,
    incidencias_sla INTEGER DEFAULT 0,
    oportunidades_detectadas INTEGER DEFAULT 0
);

-- Tabla cohortes_investigacion (anonimizada)
CREATE TABLE cohortes_investigacion (
    cohorte_id SERIAL PRIMARY KEY,
    paciente_id TEXT, -- FK opcional, puede ser anonimizado
    edad INTEGER,
    ciudad TEXT,
    aseguramiento TEXT,
    programa_clinico TEXT,
    problema_seleccionado INTEGER,
    nivel_riesgo nivel_riesgo_enum,
    score_total INTEGER,
    fenotipo_probable TEXT,
    cie10 TEXT,
    fecha_registro TIMESTAMPTZ DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_conversaciones_paciente ON conversaciones(paciente_id);
CREATE INDEX idx_conversaciones_telefono ON conversaciones(telefono);
CREATE INDEX idx_escalamientos_paciente ON escalamientos(paciente_id, timestamp_escalamiento);
CREATE INDEX idx_na_interacciones_paciente ON neuroasistente_interacciones(paciente_id, estado_interaccion);
CREATE INDEX idx_na_interacciones_fecha ON neuroasistente_interacciones(fecha_hora);
CREATE INDEX idx_pacientes_fase ON pacientes(fase_actual);
CREATE INDEX idx_pacientes_riesgo ON pacientes(nivel_riesgo);
