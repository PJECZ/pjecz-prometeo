"""
Listas de Acuerdos v3, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from lib.authentications import Usuario, get_current_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

from .crud import get_listas_de_acuerdos
from .schemas import ListaDeAcuerdoOut

listas_de_acuerdos = APIRouter(prefix="/v3/listas_de_acuerdos", tags=["listas de acuerdos"])


@listas_de_acuerdos.get("/{lista_de_acuerdo_id}", response_model=ListaDeAcuerdoOut)
async def detalle_lista_de_acuerdo(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    lista_de_acuerdo_id: int,
):
    """Detalle de una lista de acuerdo a partir de su id"""
    try:
        lista_de_acuerdo = get_listas_de_acuerdos(db, lista_de_acuerdo_id)
    except MyAnyError as error:
        return ListaDeAcuerdoOut(success=False, message=str(error))
    return ListaDeAcuerdoOut.model_validate(lista_de_acuerdo)
