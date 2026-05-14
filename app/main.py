from fastapi import FastAPI

app = FastAPI(title="NeurOrientador ICN Salud", version="6.0")

from app.routers.webhook import webhook_router
from app.routers.health import health_router
from app.routers.admin import admin_router

app.include_router(webhook_router, prefix="/webhook")
app.include_router(health_router)
app.include_router(admin_router, prefix="/admin")
