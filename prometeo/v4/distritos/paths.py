"""
Distritos v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.authentications import Usuario, get_current_userdev, get_current_username
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList

from .crud import get_distrito_with_clave, get_distritos
from .schemas import DistritoOut, OneDistritoOut

distritos = APIRouter(prefix="/v4/distritos", tags=["distritos"])


@distritos.get("/listado", response_model=CustomList[DistritoOut])
async def listado_distritos(
    database: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_userdev)],
    es_distrito_judicial: bool = None,
    es_distrito: bool = None,
    es_jurisdiccional: bool = None,
):
    """Listado de distritos"""
    try:
        query = get_distritos(
            database=database,
            es_distrito_judicial=es_distrito_judicial,
            es_distrito=es_distrito,
            es_jurisdiccional=es_jurisdiccional,
        )
    except MyAnyError as error:
        return CustomList(success=False, message=str(error))
    return paginate(query)


@distritos.get("/{distrito_clave}", response_model=OneDistritoOut)
async def detalle_distrito(
    database: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_username)],
    distrito_clave: str,
):
    """Detalle de un distrito a partir de su clave"""
    try:
        distrito = get_distrito_with_clave(database, distrito_clave)
    except MyAnyError as error:
        return OneDistritoOut(success=False, message=str(error))
    return OneDistritoOut.model_validate(distrito)
