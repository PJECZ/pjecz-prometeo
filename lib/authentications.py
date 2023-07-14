"""
Autentificaciones
"""
from typing import Annotated
import re

from cryptography.fernet import Fernet
from fastapi import HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel

from config.settings import Settings, get_settings

EMAIL_REGEXP = r"^[\w.-]+@[\w.-]+\.\w+$"
X_API_KEY = APIKeyHeader(name="X-Api-Key")


def encrypt_email(
    settings: Annotated[Settings, Depends(get_settings)],
    email: str,
) -> str:
    """Encriptar email"""

    return Fernet(settings.fernet_key).encrypt(email.encode()).decode()


def decrypt_email(
    settings: Annotated[Settings, Depends(get_settings)],
    email: str,
) -> str:
    """Desencriptar email"""

    return Fernet(settings.fernet_key).decrypt(email.encode()).decode()


class Usuario(BaseModel):
    """Usuario"""

    api_key: str
    email: str


async def get_current_user(
    settings: Annotated[Settings, Depends(get_settings)],
    api_key: str = Depends(X_API_KEY),
) -> Usuario:
    """Obtener usuario actual"""

    # Desencriptar api_key para obtener email
    try:
        email = decrypt_email(settings, api_key)
    except Exception as error:
        raise HTTPException(status_code=403, detail="API Key inválida")

    # Validar email
    if not re.match(EMAIL_REGEXP, email):
        raise HTTPException(status_code=403, detail="API Key inválida porque el email no es válido")
    if email != settings.username:
        raise HTTPException(status_code=403, detail="API Key no autorizada")

    # Entregar
    return Usuario(api_key=api_key, email=email)
