"""
Edictos v3, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from lib.authentications import Usuario, get_current_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

from .crud import get_edictos
from .schemas import EdictoOut, OneEdictoOut

edictos = APIRouter(prefix="/v3/edictos", tags=["edictos"])


@edictos.get("/{edicto_id}", response_model=OneEdictoOut)
async def detalle_edicto(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    edicto_id: int,
):
    """Detalle de un edicto a partir de su id"""
    try:
        edicto = get_edictos(db, edicto_id)
    except MyAnyError as error:
        return OneEdictoOut(success=False, message=str(error))
    return OneEdictoOut.model_validate(edicto)
