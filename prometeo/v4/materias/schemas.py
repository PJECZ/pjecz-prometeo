"""
Materias v4, esquemas de pydantic
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
