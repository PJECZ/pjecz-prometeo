"""
Glosas v4, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_expediente

from ...core.autoridades.models import Autoridad
from ...core.glosas.models import Glosa
from ..autoridades.crud import get_autoridad, get_autoridad_with_clave
from ..distritos.crud import get_distrito, get_distrito_with_clave


def get_glosas(
    db: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    expediente: str = None,
    anio: int = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
) -> Any:
    """Consultar los glosas activas"""
    consulta = db.query(Glosa)
    if autoridad_id is not None:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    elif autoridad_clave is not None and autoridad_clave != "":
        autoridad = get_autoridad_with_clave(db, autoridad_clave)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    elif distrito_id is not None:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.join(Autoridad).filter(Autoridad.distrito_id == distrito.id)
    elif distrito_clave is not None and distrito_clave != "":
        distrito = get_distrito_with_clave(db, distrito_clave)
        consulta = consulta.join(Autoridad).filter(Autoridad.distrito_id == distrito.id)
    if expediente is not None:
        try:
            expediente = safe_expediente(expediente)
        except (IndexError, ValueError) as error:
            raise MyNotValidParamError("El expediente no es válido") from error
        consulta = consulta.filter_by(expediente=expediente)
    if anio is not None:
        desde = date(year=anio, month=1, day=1)
        hasta = date(year=anio, month=12, day=31)
        consulta = consulta.filter(Glosa.fecha >= desde).filter(Glosa.fecha <= hasta)
    elif fecha is not None:
        consulta = consulta.filter(Glosa.fecha == fecha)
    else:
        if fecha_desde is not None:
            consulta = consulta.filter(Glosa.fecha >= fecha_desde)
        if fecha_hasta is not None:
            consulta = consulta.filter(Glosa.fecha <= fecha_hasta)
    return consulta.filter_by(estatus="A").order_by(Glosa.id)


def get_glosa(db: Session, glosa_id: int) -> Glosa:
    """Consultar una glosa por su id"""
    glosa = db.query(Glosa).get(glosa_id)
    if glosa is None:
        raise MyNotExistsError("No existe ese glosa")
    if glosa.estatus != "A":
        raise MyIsDeletedError("No es activo ese glosa, está eliminado")
    return glosa
