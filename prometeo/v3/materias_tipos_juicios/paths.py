"""
Materias-Tipos de Juicios v3, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.authentications import Usuario, get_current_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList

from .crud import get_materia_tipo_juicio, get_materias_tipos_juicios
from .schemas import MateriaTipoJuicioOut, OneMateriaTipoJuicioOut

materias_tipos_juicios = APIRouter(prefix="/v3/materias_tipos_juicios", tags=["materias - tipos de juicios"])


@materias_tipos_juicios.get("", response_model=CustomList[MateriaTipoJuicioOut])
async def listado_materias_tipos_juicios(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    materia_id: int = None,
    materia_clave: str = None,
):
    """Listado de materias-tipos de juicios"""
    query = get_materias_tipos_juicios(
        db=db,
        materia_id=materia_id,
        materia_clave=materia_clave,
    )
    return paginate(query)


@materias_tipos_juicios.get("/{materia_tipo_juicio_id}")
async def detalle_materia_tipo_juicio(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    materia_tipo_juicio_id: int,
) -> OneMateriaTipoJuicioOut:
    """Detalle de una materia-tipo de juicio a partir de su id"""
    try:
        materia_tipo_juicio = get_materia_tipo_juicio(db, materia_tipo_juicio_id)
    except MyAnyError as error:
        return OneMateriaTipoJuicioOut(success=False, message=str(error))
    return OneMateriaTipoJuicioOut.model_validate(materia_tipo_juicio)
