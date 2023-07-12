"""
Sentencias v3, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from lib.authentications import Usuario, get_current_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

from .crud import get_sentencias
from .schemas import SentenciaOut

sentencias = APIRouter(prefix="/v3/sentencias", tags=["sentencias"])


@sentencias.get("/{sentencia_id}")
async def detalle_sentencia(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    sentencia_id: int,
) -> SentenciaOut:
    """Detalle de una sentencia a partir de su id"""
    try:
        sentencia = get_sentencias(db, sentencia_id)
    except MyAnyError as error:
        return SentenciaOut(success=False, message=str(error))
    return SentenciaOut.model_validate(sentencia)
