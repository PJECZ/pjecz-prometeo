"""
Settings

Para que la configuración no sea estática en el código,
se utiliza la librería pydantic para cargar la configuración desde
Google Secret Manager como primer opción, luego de un archivo .env
que se usa en local y por último de variables de entorno.

Para desarrollo debe crear un archivo .env en la raíz del proyecto
con las siguientes variables:

- DB_HOST
- DB_PORT
- DB_NAME
- DB_PASS
- DB_USER
- FERNET_KEY
- GCP_BUCKET
- GCP_BUCKET_EDICTOS
- GCP_BUCKET_GLOSAS
- GCP_BUCKET_LISTAS_DE_ACUERDOS
- GCP_BUCKET_SENTENCIAS
- ORIGINS
- RECAPTCHA_SITE_KEY
- USERDEV
- USERNAME

Para producción vaya a Google Secret Manager en
https://console.cloud.google.com/security/secret-manager
y cree como secretos las siguientes variable de entorno

- pjecz_prometeo_api_db_host
- pjecz_prometeo_api_db_port
- pjecz_prometeo_api_db_name
- pjecz_prometeo_api_db_pass
- pjecz_prometeo_api_db_user
- pjecz_prometeo_api_fernet_key
- pjecz_prometeo_api_gcp_bucket
- pjecz_prometeo_api_gcp_bucket_edictos
- pjecz_prometeo_api_gcp_bucket_glosas
- pjecz_prometeo_api_gcp_bucket_listas_de_acuerdos
- pjecz_prometeo_api_gcp_bucket_sentencias
- pjecz_prometeo_api_origins
- pjecz_prometeo_api_recaptcha_site_key
- pjecz_prometeo_api_userdev
- pjecz_prometeo_api_username

Y en el archivo app.yaml agregue las siguientes variables de entorno

- PROJECT_ID: justicia-digital-gob-mx
- SERVICE_PREFIX: pjecz_prometeo_api
"""
import os
from functools import lru_cache

from google.cloud import secretmanager
from pydantic_settings import BaseSettings

PROJECT_ID = os.getenv("PROJECT_ID", "")  # Por defecto esta vacio, esto significa estamos en modo local
SERVICE_PREFIX = os.getenv("SERVICE_PREFIX", "pjecz_prometeo_api")


def get_secret(secret_id: str) -> str:
    """Get secret from google cloud secret manager"""

    # If not in google cloud, return environment variable
    if PROJECT_ID == "":
        return os.getenv(secret_id.upper(), "")

    # Create the secret manager client
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    secret = f"{SERVICE_PREFIX}_{secret_id}"
    name = client.secret_version_path(PROJECT_ID, secret, "latest")

    # Access the secret version
    response = client.access_secret_version(name=name)

    # Return the decoded payload
    return response.payload.data.decode("UTF-8")


class Settings(BaseSettings):
    """Settings"""

    db_host: str = get_secret("db_host")
    db_port: int = get_secret("db_port")
    db_name: str = get_secret("db_name")
    db_pass: str = get_secret("db_pass")
    db_user: str = get_secret("db_user")
    fernet_key: str = get_secret("fernet_key")
    gcp_bucket: str = get_secret("gcp_bucket")
    gcp_bucket_edictos: str = get_secret("gcp_bucket_edictos")
    gcp_bucket_glosas: str = get_secret("gcp_bucket_glosas")
    gcp_bucket_listas_de_acuerdos: str = get_secret("gcp_bucket_listas_de_acuerdos")
    gcp_bucket_sentencias: str = get_secret("gcp_bucket_sentencias")
    origins: str = get_secret("origins")
    recaptcha_site_key: str = get_secret("recaptcha_site_key")
    tz: str = "America/Mexico_City"
    userdev: str = get_secret("userdev")
    username: str = get_secret("username")

    class Config:
        """Load configuration"""

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            """Customise sources, first environment variables, then .env file, then google cloud secret manager"""
            return env_settings, file_secret_settings, init_settings


@lru_cache()
def get_settings() -> Settings:
    """Get Settings"""
    return Settings()


# CurrentSettings = Annotated[Settings, Depends(get_settings)]
