"""
Edictos v4, rutas (paths)
"""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.authentications import Usuario, get_current_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from .crud import get_edictos, get_edicto
from .schemas import EdictoOut, OneEdictoOut

edictos = APIRouter(prefix="/v4/edictos", tags=["edictos"])


@edictos.get("", response_model=CustomPage[EdictoOut])
async def listado_edictos(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    anio: int = None,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    expediente: str = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
):
    """Listado de edictos"""
    try:
        query = get_edictos(
            db=db,
            anio=anio,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            expediente=expediente,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(query)


@edictos.get("/{edicto_id}", response_model=OneEdictoOut)
async def detalle_edicto(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    edicto_id: int,
):
    """Detalle de un edicto a partir de su id"""
    try:
        edicto = get_edicto(db, edicto_id)
    except MyAnyError as error:
        return OneEdictoOut(success=False, message=str(error))
    return OneEdictoOut.model_validate(edicto)
