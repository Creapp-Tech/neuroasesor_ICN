from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base

class Appointment(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(String(30), nullable=False)
    programa = Column(String(50))
    tipo_cita = Column(String(100))
    fecha_propuesta = Column(String(100))
    estado = Column(String(30), default="pendiente")
    notas = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())