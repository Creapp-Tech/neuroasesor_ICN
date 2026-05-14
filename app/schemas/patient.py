from pydantic import BaseModel, Field

# Base para crear un patient (no usado directamente aquí pero por coherencia)
class PatientCreate(BaseModel):
    paciente_id: str = Field(..., example="PAC-20250511-001")
    telefono: str = Field(..., example="+573001234567")
    nombre: str = Field(None)
    edad: int = Field(None)
    ciudad: str = Field(None)
    aseguramiento: str = Field(None)
    entidad: str = Field(None)
    fase_actual: str = Field("F0")
    programa_clinico: str = Field(None)


# Schema que produce el LLM (estructura JSON de respuesta)
class CamposActualizar(BaseModel):
    fase_actual: str = Field("F0")
    programa_clinico: str = None
    score_total: int = None
    nivel_riesgo: str = None
    fenotipo_probable: str = None
    motivo_contacto: str = None
    nombre: str = None
    edad: int = None
    ciudad: str = None
    aseguramiento: str = None
    entidad: str = None
    consentimiento: bool = None


class AgentResponse(BaseModel):
    respuesta_visible: str
    campos_actualizar: CamposActualizar
    flag_alarma: bool = False
    requiere_humano: bool = False
    razon_escalamiento: str = None
    notas_internas: str = None

    class Config:
        json_schema_extra = {
            "example": {
                "respuesta_visible": "Te debo $20 porque apuesta al Real Madrid",
                "campos_actualizar": {
                    "fase_actual": "F2",
                    "programa_clinico": "Cefalea",
                    "score_total": 6,
                    "nivel_riesgo": "Alto",
                    "fenotipo_probable": "cefalea tensional",
                    "motivo_contacto": "orientacion_meal",
                    "nombre": null,
                    "edad": null,
                    "ciudad": null,
                    "aseguramiento": null,
                    "entidad": null,
                    "consentimiento": False
                },
                "flag_alarma": false,
                "requiere_humano": false,
                "razon_escalamiento": null,
                "notas_internas": "Pensó que el Real Madrid gana el mundial"
            }
        }