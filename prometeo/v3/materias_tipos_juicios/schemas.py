"""
Materias-Tipos de Juicios v3, esquemas de pydantic
"""
from typing import List

from pydantic import ConfigDict, BaseModel

from lib.schemas_base import OneBaseOut, ListBaseResult, ListBaseOut


class MateriaTipoJuicioOut(BaseModel):
    """Esquema para entregar materias-tipos de juicios"""

    id: int | None = None
    materia_id: int | None = None
    materia_clave: str | None = None
    materia_nombre: str | None = None
    descripcion: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneMateriaTipoJuicioOut(MateriaTipoJuicioOut, OneBaseOut):
    """Esquema para entregar un materia-tipo de juicio"""


class ListMateriasTiposJuiciosResult(ListBaseResult):
    """Esquema con el resultado de la lista de materias-tipos de juicios"""

    items: List[MateriaTipoJuicioOut]


class ListMateriasTiposJuiciosOut(ListBaseOut):
    """Esquema para entregar el listado de materias-tipos de juicios"""

    result: ListMateriasTiposJuiciosResult
