"""
Módulo de conexión a PostgreSQL con SQLAlchemy.
Configura el engine, pool de conexiones y sesión para FastAPI.
"""
import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

import app.config as config

logger = logging.getLogger(__name__)

# ─── Engine con pool de conexiones ────────────────────────────────
engine = create_engine(
    config.DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    connect_args={
        "connect_timeout": 30,
        # keepalives para conexiones persistentes (útil en Railway/Cloud)
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    },
    echo=False,  # True para debug de queries SQL
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base declarativa para los modelos ORM
Base = declarative_base()


# ─── Dependencia FastAPI: sesión por request ───────────────────────
def get_db() -> Generator:
    """
    Genera una sesión de base de datos por solicitud.
    Se usa como dependencia en los routers de FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─── Verificación de conexión ─────────────────────────────────────
def verify_db_connection() -> bool:
    """
    Verifica que la conexión a PostgreSQL funciona correctamente.
    Retorna True si la conexión es exitosa, False en caso contrario.
    """
    try:
        with engine.connect() as connection:
            connection.execute(engine.dialect.text("SELECT 1"))
        logger.info("✅ Conexión a PostgreSQL verificada correctamente.")
        return True
    except SQLAlchemyError as e:
        logger.error(f"❌ Error conectando a PostgreSQL: {e}")
        return False


# ─── Inicialización al importar ───────────────────────────────────
if not verify_db_connection():
    logger.warning("⚠️ No se pudo conectar a PostgreSQL al iniciar. Verifica DATABASE_URL.")