"""
Edictos v3, esquemas de pydantic
"""
from datetime import date

from pydantic import ConfigDict, BaseModel

from lib.schemas_base import OneBaseOut


class EdictoOut(BaseModel):
    """Esquema para entregar edictos"""

    id: int | None = None
    distrito_id: int | None = None
    distrito_clave: str | None = None
    distrito_nombre: str | None = None
    distrito_nombre_corto: str | None = None
    autoridad_id: int | None = None
    autoridad_clave: str | None = None
    autoridad_descripcion: str | None = None
    autoridad_descripcion_corta: str | None = None
    fecha: date | None = None
    descripcion: str | None = None
    expediente: str | None = None
    numero_publicacion: str | None = None
    archivo: str | None = None
    url: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneEdictoOut(EdictoOut, OneBaseOut):
    """Esquema para entregar un edicto"""
