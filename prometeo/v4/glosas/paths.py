"""
Glosas v4, rutas (paths)
"""
from datetime import date
from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Response
from fastapi_pagination.ext.sqlalchemy import paginate

from config.settings import Settings, get_settings
from lib.authentications import Usuario, get_current_userdev, get_current_username
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage
from lib.google_cloud_storage import get_blob_name_from_url, get_file_from_gcs, get_media_type_from_filename
from lib.recaptcha_enterprise import create_assessment

from .crud import get_glosa, get_glosas
from .schemas import GlosaOut, OneGlosaOut

glosas = APIRouter(prefix="/v4/glosas", tags=["glosas"])


@glosas.get("/descargar/{glosa_id}")
async def descargar_glosa(
    database: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_userdev)],
    settings: Annotated[Settings, Depends(get_settings)],
    background_tasks: BackgroundTasks,
    glosa_id: int,
):
    """Descargar de una glosa a partir de su id"""
    try:
        glosa = get_glosa(database, glosa_id)
        archivo_contenido = get_file_from_gcs(
            bucket_name=settings.gcp_bucket_glosas,
            blob_name=get_blob_name_from_url(glosa.url),
        )
        archivo_media_type = get_media_type_from_filename(glosa.archivo)
    except MyAnyError as error:
        return OneGlosaOut(success=False, message=str(error))
    buffer = BytesIO(archivo_contenido)
    background_tasks.add_task(buffer.close)
    headers = {"Content-Disposition": f'inline; filename="{glosa.archivo}"'}
    return Response(buffer.getvalue(), headers=headers, media_type=archivo_media_type)


@glosas.get("/recaptcha/{glosa_id}")
async def descargar_recaptcha_glosa(
    database: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_username)],
    settings: Annotated[Settings, Depends(get_settings)],
    background_tasks: BackgroundTasks,
    glosa_id: int,
    token: str,
):
    """Descargar de una glosa a partir de su id, validando reCAPTCHA"""
    await create_assessment(settings=settings, token=token)
    try:
        glosa = get_glosa(database, glosa_id)
        archivo_contenido = get_file_from_gcs(
            bucket_name=settings.gcp_bucket_glosas,
            blob_name=get_blob_name_from_url(glosa.url),
        )
        archivo_media_type = get_media_type_from_filename(glosa.archivo)
    except MyAnyError as error:
        return OneGlosaOut(success=False, message=str(error))
    buffer = BytesIO(archivo_contenido)
    background_tasks.add_task(buffer.close)
    headers = {"Content-Disposition": f'inline; filename="{glosa.archivo}"'}
    return Response(buffer.getvalue(), headers=headers, media_type=archivo_media_type)


@glosas.get("/paginado", response_model=CustomPage[GlosaOut])
async def listado_glosas(
    database: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_userdev)],
    autoridad_id: int = None,
    autoridad_clave: str = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    expediente: str = None,
    anio: int = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
):
    """Listado de glosas"""
    try:
        query = get_glosas(
            database=database,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            expediente=expediente,
            anio=anio,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(query)


@glosas.get("/{glosa_id}", response_model=OneGlosaOut)
async def detalle_glosa(
    database: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_username)],
    glosa_id: int,
):
    """Detalle de una glosa a partir de su id"""
    try:
        glosa = get_glosa(database, glosa_id)
    except MyAnyError as error:
        return OneGlosaOut(success=False, message=str(error))
    return OneGlosaOut.model_validate(glosa)
