"""
Materias v3, esquemas de pydantic
"""
from pydantic import ConfigDict, BaseModel

from lib.schemas_base import OneBaseOut


class MateriaOut(BaseModel):
    """Esquema para entregar materias"""

    id: int | None = None
    clave: str | None = None
    nombre: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneMateriaOut(MateriaOut, OneBaseOut):
    """Esquema para entregar una materia"""


class ListMateriasResult(BaseModel):
    """Esquema con el resultado de la lista de materias"""

    total: int
    items: list[MateriaOut]
    size: int


class ListMateriasOut(BaseModel):
    """Esquema para entregar el listado de materias"""

    success: bool = True
    message: str = "Success"
    result: ListMateriasResult
