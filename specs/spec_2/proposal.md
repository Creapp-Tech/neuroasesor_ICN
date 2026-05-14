# Spec 2 — db_repository.py + models.py: Repositorio PostgreSQL y Modelos ORM

## Qué resuelve
Implementa toda la capa de persistencia del sistema usando PostgreSQL como base de datos relacional. Define los modelos ORM con SQLAlchemy y la clase `DBRepository` con operaciones CRUD para todas las entidades del sistema: pacientes, conversaciones, citas, escalamientos, interacciones del NeuroAsistente y Neuroasesor, y resúmenes diarios.

## Por qué es necesaria
PostgreSQL reemplaza a Google Sheets como base de datos operativa. Sin esta capa ningún módulo del sistema puede leer ni persistir datos. Centraliza el acceso a datos con conexión async (asyncpg), control de duplicados por teléfono (clave primaria de pacientes), integridad referencial entre tablas y manejo transaccional correcto.

## Qué entrega
- `models.py`: tablas SQLAlchemy ORM (PACIENTES, CONVERSACIONES, CITAS, ESCALAMIENTOS, NEUROASISTENTE_INTERACCIONES, NEUROASESOR_INTERACCIONES, RESUMENES_DIARIOS, COHORTES_INVESTIGACION) con todos los campos definidos en V6.
- `db_repository.py`: clase `DBRepository` con métodos CRUD para cada entidad, conexión async con `DATABASE_URL` de `config.py`, y validación de consentimiento antes de insertar en COHORTES.
- `migrations/`: configuración de Alembic para versionado del esquema.
