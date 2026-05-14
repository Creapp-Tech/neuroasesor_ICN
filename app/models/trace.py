from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import db

class Trace(db):
    __tablename__ = "trazabilidad"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(String(30), nullable=False)
    evento = Column(String(100))  # fase_cambio | alarma | escalamiento | json_retry
    detalle = Column(Text)
    valor_anterior = Column(String(200))
    valor_nuevo = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())