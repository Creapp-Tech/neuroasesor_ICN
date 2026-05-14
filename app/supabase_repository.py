import time
from datetime import date, datetime, timedelta
from typing import List, Optional

from supabase import create_client, Client
from postgrest.exceptions import APIError

from app import config
from app.schemas import (
    Paciente, Conversacion, Cita, Escalamiento,
    NeuroAsistenteInteraccion, NeuroAsesorInteraccion, ResumenDiario
)

_MAX_RETRIES = 3
_BACKOFF_BASE = 2  # seconds; delay = base ** attempt


class SupabaseRepository:
    """Repository for interacting with Supabase (PostgreSQL)."""

    def __init__(self):
        self.client: Client = create_client(
            config.SUPABASE_URL,
            config.SUPABASE_SERVICE_KEY
        )

    def _retry(self, func, *args, **kwargs):
        """Retry func up to _MAX_RETRIES times with exponential backoff on APIError."""
        for attempt in range(_MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except APIError:
                if attempt == _MAX_RETRIES - 1:
                    raise
                time.sleep(_BACKOFF_BASE ** (attempt + 1))

    # ── Pacientes ────────────────────────────────────────────────────────────

    def get_paciente_by_telefono(self, telefono: str) -> Optional[Paciente]:
        """Retrieve a patient by WhatsApp phone number. Returns None if not found."""
        try:
            response = (
                self.client.table("pacientes")
                .select("*")
                .eq("telefono", telefono)
                .maybe_single()
                .execute()
            )
            if response.data:
                return Paciente(**response.data)
            return None
        except APIError as e:
            # PGRST116 = "no rows returned" — treat as not found
            if "PGRST116" in str(e):
                return None
            raise

    def create_paciente(self, paciente: Paciente) -> Paciente:
        """Insert a new patient record."""
        data = paciente.model_dump(mode="json")
        response = self._retry(
            lambda: self.client.table("pacientes").insert(data).execute()
        )
        return Paciente(**response.data[0])

    def update_paciente(self, telefono: str, campos: dict) -> None:
        """Update specific fields of a patient record. Always stamps ultima_actividad."""
        campos["ultima_actividad"] = datetime.utcnow().isoformat()
        self._retry(
            lambda: self.client.table("pacientes").update(campos).eq("telefono", telefono).execute()
        )

    def update_paciente_by_id(self, paciente_id: str, campos: dict) -> None:
        """Update specific fields of a patient record by paciente_id."""
        campos["ultima_actividad"] = datetime.utcnow().isoformat()
        self._retry(
            lambda: self.client.table("pacientes").update(campos).eq("paciente_id", paciente_id).execute()
        )

    # ── Conversaciones ───────────────────────────────────────────────────────

    def insert_conversacion(self, conv: Conversacion) -> None:
        """Log a conversation turn."""
        data = conv.model_dump(mode="json")
        self._retry(
            lambda: self.client.table("conversaciones").insert(data).execute()
        )

    def get_conversaciones_by_paciente_id(self, paciente_id: str) -> List[Conversacion]:
        """Return all conversation turns for a patient ordered by timestamp."""
        response = (
            self.client.table("conversaciones")
            .select("*")
            .eq("paciente_id", paciente_id)
            .order("timestamp", desc=False)
            .execute()
        )
        return [Conversacion(**item) for item in response.data]

    # ── Citas ────────────────────────────────────────────────────────────────

    def insert_cita(self, cita: Cita) -> None:
        """Register a new appointment."""
        data = cita.model_dump(mode="json")
        self._retry(
            lambda: self.client.table("citas").insert(data).execute()
        )

    def update_cita(self, cita_id: str, campos: dict) -> None:
        """Update appointment details."""
        self._retry(
            lambda: self.client.table("citas").update(campos).eq("cita_id", cita_id).execute()
        )

    def get_citas_pendientes_seguimiento(self) -> List[Cita]:
        """Return appointments from yesterday that haven't had post-follow-up yet."""
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        response = (
            self.client.table("citas")
            .select("*")
            .eq("fecha_cita", yesterday)
            .eq("seguimiento_post", False)
            .eq("confirmacion", "Confirmada")
            .execute()
        )
        return [Cita(**item) for item in response.data]

    # ── Escalamientos ────────────────────────────────────────────────────────

    def insert_escalamiento(self, esc: Escalamiento) -> None:
        """Log a new human escalation."""
        data = esc.model_dump(mode="json")
        self._retry(
            lambda: self.client.table("escalamientos").insert(data).execute()
        )

    def update_escalamiento(self, escalamiento_id: str, campos: dict) -> None:
        """Update escalation details (e.g. response timestamp, resolution)."""
        self._retry(
            lambda: self.client.table("escalamientos")
            .update(campos)
            .eq("escalamiento_id", escalamiento_id)
            .execute()
        )

    def get_escalamientos_sin_respuesta(self) -> List[Escalamiento]:
        """Retrieve escalations still waiting for human response."""
        response = (
            self.client.table("escalamientos")
            .select("*")
            .is_("timestamp_respuesta_humano", "null")
            .execute()
        )
        return [Escalamiento(**item) for item in response.data]

    def get_escalamiento_by_id(self, escalamiento_id: str) -> Optional[Escalamiento]:
        """Return a single escalation by its primary key."""
        try:
            response = (
                self.client.table("escalamientos")
                .select("*")
                .eq("escalamiento_id", escalamiento_id)
                .maybe_single()
                .execute()
            )
            if response.data:
                return Escalamiento(**response.data)
            return None
        except APIError as e:
            if "PGRST116" in str(e):
                return None
            raise

    def get_escalamientos_del_dia(self, fecha: date) -> List[Escalamiento]:
        """Return all escalations created on the given date (UTC day boundaries)."""
        start = f"{fecha.isoformat()}T00:00:00Z"
        end = f"{fecha.isoformat()}T23:59:59Z"
        response = (
            self.client.table("escalamientos")
            .select("*")
            .gte("timestamp_escalamiento", start)
            .lte("timestamp_escalamiento", end)
            .execute()
        )
        return [Escalamiento(**item) for item in response.data]

    # ── NeuroAsistente ───────────────────────────────────────────────────────

    def insert_neuroasistente_interaccion(self, i: NeuroAsistenteInteraccion) -> None:
        """Log a NeuroAsistente interaction."""
        data = i.model_dump(mode="json")
        self._retry(
            lambda: self.client.table("neuroasistente_interacciones").insert(data).execute()
        )

    def update_neuroasistente_interaccion(self, interaccion_id: str, campos: dict) -> None:
        """Update NeuroAsistente interaction state."""
        campos["timestamp_actualizacion"] = datetime.utcnow().isoformat()
        self._retry(
            lambda: self.client.table("neuroasistente_interacciones")
            .update(campos)
            .eq("interaccion_id", interaccion_id)
            .execute()
        )

    def get_interacciones_del_dia(self, fecha: date) -> List[NeuroAsistenteInteraccion]:
        """Get all NeuroAsistente interactions for a specific date (UTC day boundaries)."""
        start = f"{fecha.isoformat()}T00:00:00Z"
        end = f"{fecha.isoformat()}T23:59:59Z"
        response = (
            self.client.table("neuroasistente_interacciones")
            .select("*")
            .gte("fecha_hora", start)
            .lte("fecha_hora", end)
            .execute()
        )
        return [NeuroAsistenteInteraccion(**item) for item in response.data]

    def get_neuroasistente_interaccion_by_id(
        self, interaccion_id: str
    ) -> Optional[NeuroAsistenteInteraccion]:
        """Return a single NeuroAsistente interaction by its primary key."""
        try:
            response = (
                self.client.table("neuroasistente_interacciones")
                .select("*")
                .eq("interaccion_id", interaccion_id)
                .maybe_single()
                .execute()
            )
            if response.data:
                return NeuroAsistenteInteraccion(**response.data)
            return None
        except APIError as e:
            if "PGRST116" in str(e):
                return None
            raise

    def get_interaccion_activa_por_paciente(
        self, paciente_id: str, cita_id: str
    ) -> Optional[NeuroAsistenteInteraccion]:
        """Find the most recent 'enviado' interaction for a patient+appointment pair."""
        response = (
            self.client.table("neuroasistente_interacciones")
            .select("*")
            .eq("paciente_id", paciente_id)
            .eq("cita_id", cita_id)
            .eq("estado_interaccion", "enviado")
            .order("fecha_hora", desc=True)
            .limit(1)
            .execute()
        )
        if response.data:
            return NeuroAsistenteInteraccion(**response.data[0])
        return None

    # ── NeuroAsesor & Resúmenes ──────────────────────────────────────────────

    def insert_neuroasesor_interaccion(self, i: NeuroAsesorInteraccion) -> None:
        """Log a human Neuroasesor intervention."""
        data = i.model_dump(mode="json")
        self._retry(
            lambda: self.client.table("neuroasesor_interacciones").insert(data).execute()
        )

    def insert_resumen_diario(self, r: ResumenDiario) -> None:
        """Save a daily management summary."""
        data = r.model_dump(mode="json")
        self._retry(
            lambda: self.client.table("resumenes_diarios").insert(data).execute()
        )

    # ── Investigación ────────────────────────────────────────────────────────

    def insert_cohorte_investigacion(self, paciente: Paciente) -> None:
        """Insert anonymized patient data into the research cohort.

        Only runs when explicit research consent is given. No PII (phone/name).
        """
        if not paciente.consentimiento_investigacion:
            return

        data = {
            "paciente_id": paciente.paciente_id,
            "edad": paciente.edad,
            "ciudad": paciente.ciudad,
            "aseguramiento": paciente.aseguramiento,
            "programa_clinico": paciente.programa_clinico,
            "problema_seleccionado": paciente.problema_seleccionado,
            "nivel_riesgo": paciente.nivel_riesgo,
            "score_total": paciente.score_total,
            "fenotipo_probable": paciente.fenotipo_probable,
            "cie10": paciente.cie10,
        }
        self._retry(
            lambda: self.client.table("cohortes_investigacion").insert(data).execute()
        )
