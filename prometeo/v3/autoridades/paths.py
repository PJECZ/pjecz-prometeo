"""
Autoridades v3, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from lib.authentications import Usuario, get_current_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

from .crud import get_autoridad_with_clave
from .schemas import OneAutoridadOut

autoridades = APIRouter(prefix="/v3/autoridades", tags=["autoridades"])


@autoridades.get("/{autoridad_clave}", response_model=OneAutoridadOut)
async def detalle_autoridad(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    autoridad_clave: str,
):
    """Detalle de una autoridad a partir de su clave"""
    try:
        autoridad = get_autoridad_with_clave(db, autoridad_clave)
    except MyAnyError as error:
        return OneAutoridadOut(success=False, message=str(error))
    return OneAutoridadOut.model_validate(autoridad)
