from pydantic import BaseModel, Field
from datetime import datetime

# Schema para crear un nuevo turno de conversación
class TurnCreate(BaseModel):
    paciente_id: str = Field(..., example="PAC-20250511-001")
    turno: int = Field(..., ge=1)
    fase: str = Field(..., example="F0")
    rol: str = Field(..., example="paciente")
    mensaje: str = Field(..., min_length=1)
    llm_provider: str = Field(None, example="claude")  # claude | openai | gemini


# Schema para salida de conversación (con toda la información)
class TurnOut(BaseModel):
    id: int
    paciente_id: str
    turno: int
    fase: str
    rol: str
    mensaje: str
    llm_provider: str = None
    tokens_usados: int = None
    latencia_ms: int = None
    json_valido: bool = None
    created_at: datetime

    class Config:
        from_attributes = True


# Schema para historial de conversación (solo los mensajes relevantes)
class ConversationHistory(BaseModel):
    paciente_id: str
    turnos: list[TurnOut] = Field(default_factory=list)
    total_turnos: int = 0


# Respuesta estándar para conversaciones (con historial actualizado)
class ConversationResponse(BaseModel):
    message: str
    turn_id: int
    next_phase: str = None
    history: ConversationHistory = None