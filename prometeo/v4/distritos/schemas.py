"""
Distritos v4, esquemas de pydantic
"""
from typing import List

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class DistritoOut(BaseModel):
    """Esquema para entregar distritos"""

    id: int | None = None
    clave: str | None = None
    nombre: str | None = None
    nombre_corto: str | None = None
    es_distrito_judicial: bool | None = None
    es_distrito: bool | None = None
    es_jurisdiccional: bool | None = None
    model_config = ConfigDict(from_attributes=True)


class OneDistritoOut(DistritoOut, OneBaseOut):
    """Esquema para entregar un distrito"""
