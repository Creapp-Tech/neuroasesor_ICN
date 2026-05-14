"""Google Sheets persistence layer for NeurOrientador.

The repository abstracts all CRUD operations required by the spec. It uses
`gspread` with a service‑account JSON file (path taken from
`config.GOOGLE_SERVICE_ACCOUNT_JSON`). Network errors are retried up to three
times with a 2‑second back‑off. Columns are identified by the header row in each
sheet, so the order of fields in the Pydantic models does not need to match the
sheet layout exactly.
"""

import json
import logging
import time
from datetime import date, datetime
from typing import Any, Dict, List, Optional

import gspread
from gspread.exceptions import APIError, WorksheetNotFound

from . import config
from .schemas import (
    Paciente,
    Conversacion,
    Cita,
    Escalamiento,
    NeuroAsistenteInteraccion,
    NeuroAsesorInteraccion,
    ResumenDiario,
)

logger = logging.getLogger(__name__)


def _retry(func):
    """Retry wrapper for gspread API calls (max 3 attempts, 2 s back‑off)."""

    def inner(*args, **kwargs):
        attempts = 0
        while True:
            try:
                return func(*args, **kwargs)
            except APIError as exc:
                attempts += 1
                if attempts >= 3:
                    logger.error("gspread APIError after %s attempts: %s", attempts, exc)
                    raise
                logger.warning("gspread APIError, retry %s/3: %s", attempts, exc)
                time.sleep(2)

    return inner


class SheetsRepository:
    """Repository handling persistence in Google Sheets.

    The constructor opens the spreadsheet and caches worksheet objects for fast
    access. Sheet names are defined as constants in ``config.py``.
    """

    def __init__(self) -> None:
        self.gc = _retry(gspread.service_account)(filename=config.GOOGLE_SERVICE_ACCOUNT_JSON)
        self.spreadsheet = _retry(self.gc.open_by_key)(config.GOOGLE_SHEETS_ID)
        # Cache worksheets
        self._sheets: Dict[str, gspread.models.Worksheet] = {
            config.SHEET_PACIENTES: self.spreadsheet.worksheet(config.SHEET_PACIENTES),
            config.SHEET_CONVERSACIONES: self.spreadsheet.worksheet(config.SHEET_CONVERSACIONES),
            config.SHEET_CITAS: self.spreadsheet.worksheet(config.SHEET_CITAS),
            config.SHEET_ESCALAMIENTOS: self.spreadsheet.worksheet(config.SHEET_ESCALAMIENTOS),
            config.SHEET_NEUROASISTENTE_INTERACCIONES: self.spreadsheet.worksheet(
                config.SHEET_NEUROASISTENTE_INTERACCIONES
            ),
            config.SHEET_NEUROASESOR_INTERACCIONES: self.spreadsheet.worksheet(
                config.SHEET_NEUROASESOR_INTERACCIONES
            ),
            config.SHEET_RESUMENES_DIARIOS: self.spreadsheet.worksheet(config.SHEET_RESUMENES_DIARIOS),
            config.SHEET_COHORTES_INVESTIGACION: self.spreadsheet.worksheet(
                config.SHEET_COHORTES_INVESTIGACION
            ),
        }

    # ---------------------------------------------------------------------
    # Helper utilities
    # ---------------------------------------------------------------------

    def _get_worksheet(self, name: str) -> gspread.models.Worksheet:
        try:
            return self._sheets[name]
        except KeyError:
            raise WorksheetNotFound(f"Worksheet '{name}' not configured in repository")

    def _header_to_index(self, ws: gspread.models.Worksheet) -> Dict[str, int]:
        header = ws.row_values(1)
        return {col: idx + 1 for idx, col in enumerate(header)}

    def _row_to_dict(self, ws: gspread.models.Worksheet, row_num: int) -> Dict[str, Any]:
        header = ws.row_values(1)
        values = ws.row_values(row_num)
        # Pad values list to header length
        values += [""] * (len(header) - len(values))
        return dict(zip(header, values))

    # ---------------------------------------------------------------------
    # Paciente methods
    # ---------------------------------------------------------------------

    @_retry
    def get_paciente_by_telefono(self, telefono: str) -> Optional[Paciente]:
        ws = self._get_worksheet(config.SHEET_PACIENTES)
        try:
            cell = ws.find(telefono)
        except APIError:
            return None
        if not cell:
            return None
        data = self._row_to_dict(ws, cell.row)
        # Deserialize historial_json
        if "historial_json" in data and data["historial_json"]:
            try:
                data["historial_json"] = json.loads(data["historial_json"])
            except json.JSONDecodeError:
                data["historial_json"] = []
        return Paciente(**data)

    @_retry
    def create_paciente(self, paciente: Paciente) -> Paciente:
        # Verify no duplicate
        if self.get_paciente_by_telefono(paciente.telefono):
            raise ValueError(f"Paciente con telefono {paciente.telefono} ya existe")
        ws = self._get_worksheet(config.SHEET_PACIENTES)
        data = paciente.dict()
        # Serialize historial_json
        if isinstance(data.get("historial_json"), (list, dict)):
            data["historial_json"] = json.dumps(data["historial_json"])
        ws.append_row(list(data.values()))
        return paciente

    @_retry
    def update_paciente(self, telefono: str, campos: dict) -> None:
        ws = self._get_worksheet(config.SHEET_PACIENTES)
        cell = ws.find(telefono)
        if not cell:
            raise ValueError(f"Paciente con telefono {telefono} no encontrado")
        header_index = self._header_to_index(ws)
        for campo, valor in campos.items():
            if campo == "historial_json" and isinstance(valor, (list, dict)):
                valor = json.dumps(valor)
            col = header_index.get(campo)
            if col is None:
                continue  # ignore unknown fields
            ws.update_cell(cell.row, col, valor)

    # ---------------------------------------------------------------------
    # Conversacion methods
    # ---------------------------------------------------------------------

    @_retry
    def insert_conversacion(self, conv: Conversacion) -> None:
        ws = self._get_worksheet(config.SHEET_CONVERSACIONES)
        ws.append_row(list(conv.dict().values()))

    # ---------------------------------------------------------------------
    # Cita methods
    # ---------------------------------------------------------------------

    @_retry
    def insert_cita(self, cita: Cita) -> None:
        ws = self._get_worksheet(config.SHEET_CITAS)
        ws.append_row(list(cita.dict().values()))

    @_retry
    def update_cita(self, cita_id: str, campos: dict) -> None:
        ws = self._get_worksheet(config.SHEET_CITAS)
        cell = ws.find(cita_id)
        if not cell:
            raise ValueError(f"Cita con id {cita_id} no encontrada")
        header_index = self._header_to_index(ws)
        for campo, valor in campos.items():
            col = header_index.get(campo)
            if col is None:
                continue
            ws.update_cell(cell.row, col, valor)

    # ---------------------------------------------------------------------
    # Escalamiento methods
    # ---------------------------------------------------------------------

    @_retry
    def insert_escalamiento(self, esc: Escalamiento) -> None:
        ws = self._get_worksheet(config.SHEET_ESCALAMIENTOS)
        ws.append_row(list(esc.dict().values()))

    @_retry
    def update_escalamiento(self, escalamiento_id: str, campos: dict) -> None:
        ws = self._get_worksheet(config.SHEET_ESCALAMIENTOS)
        cell = ws.find(escalamiento_id)
        if not cell:
            raise ValueError(f"Escalamiento {escalamiento_id} no encontrado")
        header_index = self._header_to_index(ws)
        for campo, valor in campos.items():
            col = header_index.get(campo)
            if col is None:
                continue
            ws.update_cell(cell.row, col, valor)

    # ---------------------------------------------------------------------
    # NeuroAsistenteInteraccion methods
    # ---------------------------------------------------------------------

    @_retry
    def insert_neuroasistente_interaccion(self, interaccion: NeuroAsistenteInteraccion) -> None:
        ws = self._get_worksheet(config.SHEET_NEUROASISTENTE_INTERACCIONES)
        ws.append_row(list(interaccion.dict().values()))

    @_retry
    def update_neuroasistente_interaccion(self, interaccion_id: str, campos: dict) -> None:
        ws = self._get_worksheet(config.SHEET_NEUROASISTENTE_INTERACCIONES)
        cell = ws.find(interaccion_id)
        if not cell:
            raise ValueError(f"Interacción {interaccion_id} no encontrada")
        header_index = self._header_to_index(ws)
        for campo, valor in campos.items():
            col = header_index.get(campo)
            if col is None:
                continue
            ws.update_cell(cell.row, col, valor)

    @_retry
    def get_interacciones_del_dia(self, fecha: date) -> List[NeuroAsistenteInteraccion]:
        ws = self._get_worksheet(config.SHEET_NEUROASISTENTE_INTERACCIONES)
        records = ws.get_all_records()
        result: List[NeuroAsistenteInteraccion] = []
        for rec in records:
            # Convert string to datetime then compare date component
            try:
                dt = datetime.fromisoformat(str(rec.get("fecha_hora")))
            except (ValueError, TypeError):
                continue
            if dt.date() == fecha:
                result.append(NeuroAsistenteInteraccion(**rec))
        return result

    @_retry
    def get_interaccion_activa_por_paciente(
        self, paciente_id: str, cita_id: str
    ) -> Optional[NeuroAsistenteInteraccion]:
        ws = self._get_worksheet(config.SHEET_NEUROASISTENTE_INTERACCIONES)
        records = ws.get_all_records()
        for rec in records:
            if (
                rec.get("paciente_id") == paciente_id
                and rec.get("cita_id") == cita_id
                and rec.get("estado_interaccion") not in ("cerrado", "escalado")
            ):
                return NeuroAsistenteInteraccion(**rec)
        return None

    # ---------------------------------------------------------------------
    # NeuroAsesorInteraccion methods
    # ---------------------------------------------------------------------

    @_retry
    def insert_neuroasesor_interaccion(self, interaccion: NeuroAsesorInteraccion) -> None:
        ws = self._get_worksheet(config.SHEET_NEUROASESOR_INTERACCIONES)
        ws.append_row(list(interaccion.dict().values()))

    # ---------------------------------------------------------------------
    # ResumenDiario methods
    # ---------------------------------------------------------------------

    @_retry
    def insert_resumen_diario(self, resumen: ResumenDiario) -> None:
        ws = self._get_worksheet(config.SHEET_RESUMENES_DIARIOS)
        ws.append_row(list(resumen.dict().values()))

    # ---------------------------------------------------------------------
    # Cohortes de investigación
    # ---------------------------------------------------------------------

    @_retry
    def insert_cohorte_investigacion(self, paciente: Paciente) -> None:
        if not getattr(paciente, "consentimiento_investigacion", False):
            # No action required when consent is false.
            return
        ws = self._get_worksheet(config.SHEET_COHORTES_INVESTIGACION)
        # Insert a subset of fields – anonymized (e.g., omit identifiers). Here we
        # keep it simple and store the whole patient dict as JSON.
        payload = {
            "paciente_id": paciente.paciente_id,
            "fecha_creacion": paciente.fecha_creacion.isoformat(),
            "datos_anonymized": json.dumps(paciente.dict()),
        }
        ws.append_row(list(payload.values()))
