"""
Glosas v3, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from lib.authentications import Usuario, get_current_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

from .crud import get_glosas
from .schemas import GlosaOut, OneGlosaOut

glosas = APIRouter(prefix="/v3/glosas", tags=["glosas"])


@glosas.get("/{glosa_id}", response_model=OneGlosaOut)
async def detalle_glosa(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    glosa_id: int,
):
    """Detalle de una glosa a partir de su id"""
    try:
        glosa = get_glosas(db, glosa_id)
    except MyAnyError as error:
        return OneGlosaOut(success=False, message=str(error))
    return OneGlosaOut.model_validate(glosa)
