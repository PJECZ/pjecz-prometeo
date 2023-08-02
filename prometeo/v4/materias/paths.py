"""
Materias v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.authentications import Usuario, get_current_userdev, get_current_username
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList

from .crud import get_materia_with_clave, get_materias
from .schemas import MateriaOut, OneMateriaOut

materias = APIRouter(prefix="/v4/materias", tags=["materias"])


@materias.get("/listado", response_model=CustomList[MateriaOut])
async def listado_materias(
    database: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_userdev)],
):
    """Listado de materias"""
    try:
        query = get_materias(database)
    except MyAnyError as error:
        return CustomList(success=False, message=str(error))
    return paginate(query)


@materias.get("/{materia_clave}", response_model=OneMateriaOut)
async def detalle_materia(
    database: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_username)],
    materia_clave: str,
):
    """Detalle de una materia a partir de su id"""
    try:
        materia = get_materia_with_clave(database, materia_clave)
    except MyAnyError as error:
        return OneMateriaOut(success=False, message=str(error))
    return OneMateriaOut.model_validate(materia)
