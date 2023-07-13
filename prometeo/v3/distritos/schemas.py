"""
Distritos v3, esquemas de pydantic
"""
from typing import List

from pydantic import ConfigDict, BaseModel

from lib.schemas_base import OneBaseOut, ListBaseResult, ListBaseOut


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


class ListDistritosResult(ListBaseResult):
    """Esquema con el resultado de la lista de distritos"""

    items: List[DistritoOut]


class ListDistritosOut(ListBaseOut):
    """Esquema para entregar el listado de distritos"""

    result: ListDistritosResult
