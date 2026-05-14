# neuro-agente

## Descripción
Aplicación para gestionar interacciones con modelos de inteligencia artificial. Integra servicios de LLM (como Google Generative AI y Anthropic) con capabilidades de procesamiento de lenguaje natural para tareas de neurociencia y biotecnología.

## Características
- Interfaz API REST con FastAPI
- Soporte para múltiples proveedores de LLM
- Integración con base de datos PostgreSQL
- Sistema de autenticación y gestión de sesiones
- Pipeline de procesamiento de datos neurocognitivos

## Requisitos
Install required dependencies:
```
pip install -r requirements.txt
```

Ejemplos clave en `requirements.txt`:
- `google-generativeai` para integración con Gemini
- `anthropic` para uso de Claude
- `fastapi` y `uvicorn` para el servidor web

## Estructura del Proyecto
```
.
├── app/
│   ├── llm_client.py      # Cliente LLM para gestionar sesiones
│   └── (otros endpoints)
├── specs/
│   ├── (documentación técnica)
├── migrations/
│   └── (scripts de BD)
├── .env                  
├── Dockerfile            
└── (mas acciones)
```

## Configuración

### Variables de entorno

1. Copia el archivo de plantilla `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```
2. Abre `.env` y completa cada variable con tus propias credenciales (API keys, tokens, URLs, etc.).
3. **No modifiques `.env.example`** — es solo una plantilla para referencia.

> ⚠️ `.env` contiene credenciales reales y **no debe compartirse ni subirse al repositorio** (ya está en `.gitignore`).

### Ejecución
1. Instala dependencias: `pip install -r requirements.txt`
2. (Opcional) Inicia con Docker: `docker-compose up`
3. Inicia el servidor: `uvicorn app.main:app --reload`

## Documentación Técnica
Ver especificaciones detalladas en el directorio [`specs/`](specs/)

## Soportes Legales
- Supabase: Base de datos
- Twilio: Notificaciones SMS (si aplica)
- Anthropic/Gemini: Proveedores de LLM

\n---\nGenerated using Claude Code