"""
Sentencias v4, rutas (paths)
"""
from datetime import date
from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Response
from fastapi_pagination.ext.sqlalchemy import paginate

from config.settings import Settings, get_settings
from lib.authentications import Usuario, get_current_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage
from lib.google_cloud_storage import get_blob_name_from_url, get_file_from_gcs, get_media_type_from_filename
from lib.recaptcha_enterprise import create_assessment

from .crud import get_sentencia, get_sentencias
from .schemas import OneSentenciaOut, SentenciaOut

sentencias = APIRouter(prefix="/v4/sentencias", tags=["sentencias"])


@sentencias.get("/descargar/{sentencia_id}")
async def descargar_sentencia(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    settings: Annotated[Settings, Depends(get_settings)],
    background_tasks: BackgroundTasks,
    sentencia_id: int,
):
    """Descargar de una sentencia a partir de su id"""
    try:
        sentencia = get_sentencia(db, sentencia_id)
        archivo_contenido = get_file_from_gcs(
            bucket_name=settings.gcp_bucket_sentencias,
            blob_name=get_blob_name_from_url(sentencia.url),
        )
        archivo_media_type = get_media_type_from_filename(sentencia.archivo)
    except MyAnyError as error:
        return OneSentenciaOut(success=False, message=str(error))
    buffer = BytesIO(archivo_contenido)
    background_tasks.add_task(buffer.close)
    headers = {"Content-Disposition": f'inline; filename="{sentencia.archivo}"'}
    return Response(buffer.getvalue(), headers=headers, media_type=archivo_media_type)


@sentencias.get("/recaptcha/{sentencia_id}")
async def descargar_recaptcha_sentencia(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    settings: Annotated[Settings, Depends(get_settings)],
    background_tasks: BackgroundTasks,
    sentencia_id: int,
    token: str,
):
    """Descargar de una sentencia a partir de su id, validando reCAPTCHA"""
    await create_assessment(settings=settings, token=token)
    try:
        sentencia = get_sentencia(db, sentencia_id)
        archivo_contenido = get_file_from_gcs(
            bucket_name=settings.gcp_bucket_sentencias,
            blob_name=get_blob_name_from_url(sentencia.url),
        )
        archivo_media_type = get_media_type_from_filename(sentencia.archivo)
    except MyAnyError as error:
        return OneSentenciaOut(success=False, message=str(error))
    buffer = BytesIO(archivo_contenido)
    background_tasks.add_task(buffer.close)
    headers = {"Content-Disposition": f'inline; filename="{sentencia.archivo}"'}
    return Response(buffer.getvalue(), headers=headers, media_type=archivo_media_type)


@sentencias.get("/{sentencia_id}", response_model=OneSentenciaOut)
async def detalle_sentencia(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
    sentencia_id: int,
):
    """Detalle de una sentencia a partir de su id"""
    try:
        sentencia = get_sentencia(db, sentencia_id)
    except MyAnyError as error:
        return OneSentenciaOut(success=False, message=str(error))
    return OneSentenciaOut.model_validate(sentencia)


@sentencias.get("", response_model=CustomPage[SentenciaOut])
async def listado_sentencias(
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
    materia_tipo_juicio_id: int = None,
    sentencia: str = None,
):
    """Listado de sentencias"""
    try:
        query = get_sentencias(
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
            materia_tipo_juicio_id=materia_tipo_juicio_id,
            sentencia=sentencia,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(query)
