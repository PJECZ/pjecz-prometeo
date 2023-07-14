"""
Listas de Acuerdos v4, rutas (paths)
"""
from datetime import date
from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Response, BackgroundTasks, Depends
from fastapi_pagination.ext.sqlalchemy import paginate

from config.settings import Settings, get_settings
from lib.authentications import Usuario, get_current_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage
from lib.google_cloud_storage import get_blob_name_from_url, get_file_from_gcs, get_media_type_from_filename

from .crud import get_listas_de_acuerdos, get_lista_de_acuerdo
from .schemas import ListaDeAcuerdoOut, OneListaDeAcuerdoOut

listas_de_acuerdos = APIRouter(prefix="/v4/listas_de_acuerdos", tags=["listas de acuerdos"])


@listas_de_acuerdos.get("/descargar/{lista_de_acuerdo_id}")
async def descargar_lista_de_acuerdo(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    settings: Annotated[Settings, Depends(get_settings)],
    background_tasks: BackgroundTasks,
    lista_de_acuerdo_id: int,
):
    """Descargar de una lista de acuerdo a partir de su id"""
    try:
        lista_de_acuerdo = get_lista_de_acuerdo(db, lista_de_acuerdo_id)
        archivo_contenido = get_file_from_gcs(
            bucket_name=settings.gcp_bucket_listas_de_acuerdos,
            blob_name=get_blob_name_from_url(lista_de_acuerdo.url),
        )
        archivo_media_type = get_media_type_from_filename(lista_de_acuerdo.archivo)
    except MyAnyError as error:
        return OneListaDeAcuerdoOut(success=False, message=str(error))
    buffer = BytesIO(archivo_contenido)
    background_tasks.add_task(buffer.close)
    headers = {"Content-Disposition": f'inline; filename="{lista_de_acuerdo.archivo}"'}
    return Response(buffer.getvalue(), headers=headers, media_type=archivo_media_type)


@listas_de_acuerdos.get("/{lista_de_acuerdo_id}", response_model=OneListaDeAcuerdoOut)
async def detalle_lista_de_acuerdo(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    lista_de_acuerdo_id: int,
):
    """Detalle de una lista de acuerdo a partir de su id"""
    try:
        lista_de_acuerdo = get_lista_de_acuerdo(db, lista_de_acuerdo_id)
    except MyAnyError as error:
        return OneListaDeAcuerdoOut(success=False, message=str(error))
    return OneListaDeAcuerdoOut.model_validate(lista_de_acuerdo)


@listas_de_acuerdos.get("", response_model=CustomPage[ListaDeAcuerdoOut])
async def listado_listas_de_acuerdos(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    anio: int = None,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
):
    """Listado de listas de acuerdos"""
    try:
        query = get_listas_de_acuerdos(
            db=db,
            anio=anio,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(query)
