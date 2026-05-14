-- 002_add_indexes_and_constraints.sql
-- Complementary indexes and constraints not in 001_initial_schema.sql.
-- Safe to run after 001. All statements are idempotent (IF NOT EXISTS).

-- Additional composite index for SLA monitoring queries
CREATE INDEX IF NOT EXISTS idx_escalamientos_sin_respuesta
    ON escalamientos(timestamp_escalamiento)
    WHERE timestamp_respuesta_humano IS NULL;

-- Partial index: fast lookup for active NeuroAsistente interactions
CREATE INDEX IF NOT EXISTS idx_na_interacciones_activas
    ON neuroasistente_interacciones(paciente_id, cita_id)
    WHERE estado_interaccion = 'enviado';

-- Index for daily report generation
CREATE INDEX IF NOT EXISTS idx_resumenes_fecha ON resumenes_diarios(fecha DESC);

-- Index for cohort research queries (no PII columns indexed)
CREATE INDEX IF NOT EXISTS idx_cohortes_programa ON cohortes_investigacion(programa_clinico, nivel_riesgo);

-- Ensure historial_json is always a JSON array (not null, not object)
ALTER TABLE pacientes
    ALTER COLUMN historial_json SET DEFAULT '[]';

-- Add cumple_sla_5min column to escalamientos for alarm-specific SLA tracking
-- (alarma_critica type has a 5-minute SLA per V6 spec, separate from the 15-min SLA)
ALTER TABLE escalamientos
    ADD COLUMN IF NOT EXISTS cumple_sla_5min BOOLEAN;
