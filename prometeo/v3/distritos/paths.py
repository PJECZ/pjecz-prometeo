"""
Distritos v3, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from lib.authentications import Usuario, get_current_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

from .crud import get_distrito_with_clave, get_distritos
from .schemas import OneDistritoOut, ListDistritosResult, ListDistritosOut

distritos = APIRouter(prefix="/v3/distritos", tags=["distritos"])


@distritos.get("")
async def listado_distritos(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    es_distrito_judicial: bool = None,
    es_distrito: bool = None,
    es_jurisdiccional: bool = None,
) -> ListDistritosOut:
    """Listado de distritos"""
    query = get_distritos(
        db=db,
        es_distrito_judicial=es_distrito_judicial,
        es_distrito=es_distrito,
        es_jurisdiccional=es_jurisdiccional,
    )
    result = ListDistritosResult(total=query.count(), items=query.all(), size=query.count())
    return ListDistritosOut(result=result)


@distritos.get("/{distrito_clave}")
async def detalle_distrito(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    distrito_clave: str,
) -> OneDistritoOut:
    """Detalle de un distrito a partir de su clave"""
    try:
        distrito = get_distrito_with_clave(db, distrito_clave)
    except MyAnyError as error:
        return OneDistritoOut(success=False, message=str(error))
    return OneDistritoOut.model_validate(distrito)
