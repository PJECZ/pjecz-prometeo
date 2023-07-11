"""
Materias v3, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from lib.authentications import Usuario, get_current_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

from .crud import get_materia_with_clave
from .schemas import MateriaOut, OneMateriaOut

materias = APIRouter(prefix="/v3/materias", tags=["materias"])


@materias.get("/{materia_clave}", response_model=OneMateriaOut)
async def detalle_materia(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    materia_clave: str,
):
    """Detalle de una materia a partir de su id"""
    try:
        materia = get_materia_with_clave(db, materia_clave)
    except MyAnyError as error:
        return OneMateriaOut(success=False, message=str(error))
    return OneMateriaOut.model_validate(materia)
