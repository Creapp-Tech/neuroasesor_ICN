"""Admin endpoints — patient lookup via Supabase."""

from typing import Optional

from fastapi import APIRouter, HTTPException

from app.schemas import Paciente
from app.supabase_repository import SupabaseRepository

admin_router = APIRouter()

_repo: Optional[SupabaseRepository] = None


def _get_repo() -> SupabaseRepository:
    global _repo
    if _repo is None:
        _repo = SupabaseRepository()
    return _repo


@admin_router.get("/patients/{telefono}", response_model=Paciente)
async def get_patient(telefono: str):
    paciente = _get_repo().get_paciente_by_telefono(telefono)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente
