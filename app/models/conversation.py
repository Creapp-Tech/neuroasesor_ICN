from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base

class Conversation(Base):
    __tablename__ = "conversaciones"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(String(30), nullable=False)
    turno = Column(Integer, nullable=False)
    fase = Column(String(10))
    rol = Column(String(20))  # paciente | agente | sistema
    mensaje = Column(Text, nullable=False)
    llm_provider = Column(String(20))  # claude | openai | gemini
    tokens_usados = Column(Integer)
    latencia_ms = Column(Integer)
    json_valido = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())