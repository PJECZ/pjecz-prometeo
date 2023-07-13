"""
Autoridades v3, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from lib.authentications import Usuario, get_current_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

from .crud import get_autoridades, get_autoridad_with_clave
from .schemas import OneAutoridadOut, ListAutoridadesResult, ListAutoridadesOut

autoridades = APIRouter(prefix="/v3/autoridades", tags=["autoridades"])


@autoridades.get("")
async def listado_autoridades(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    distrito_id: int = None,
    distrito_clave: str = None,
    es_cemasc: bool = None,
    es_creador_glosas: bool = None,
    es_defensoria: bool = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    materia_id: int = None,
    materia_clave: str = None,
) -> ListAutoridadesOut:
    """Listado de autoridades"""
    query = get_autoridades(
        db=db,
        distrito_id=distrito_id,
        distrito_clave=distrito_clave,
        es_cemasc=es_cemasc,
        es_creador_glosas=es_creador_glosas,
        es_defensoria=es_defensoria,
        es_jurisdiccional=es_jurisdiccional,
        es_notaria=es_notaria,
        materia_id=materia_id,
        materia_clave=materia_clave,
    )
    result = ListAutoridadesResult(total=query.count(), items=query.all(), size=query.count())
    return ListAutoridadesOut(result=result)


@autoridades.get("/{autoridad_clave}")
async def detalle_autoridad(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    autoridad_clave: str,
) -> OneAutoridadOut:
    """Detalle de una autoridad a partir de su clave"""
    try:
        autoridad = get_autoridad_with_clave(db, autoridad_clave)
    except MyAnyError as error:
        return OneAutoridadOut(success=False, message=str(error))
    return OneAutoridadOut.model_validate(autoridad)
