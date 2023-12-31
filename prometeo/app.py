"""
PJECZ Prometeo
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi_pagination import add_pagination

from config.settings import get_settings

from .v4.autoridades.paths import autoridades
from .v4.distritos.paths import distritos
from .v4.edictos.paths import edictos
from .v4.glosas.paths import glosas
from .v4.listas_de_acuerdos.paths import listas_de_acuerdos
from .v4.materias.paths import materias
from .v4.materias_tipos_juicios.paths import materias_tipos_juicios
from .v4.sentencias.paths import sentencias


def create_app() -> FastAPI:
    """Crea la aplicación FastAPI"""

    # FastAPI
    app = FastAPI(
        title="PJECZ Prometeo",
        description="API para descargar archivos almacenados en depósitos que no son públicos. Hecho con FastAPI.",
        docs_url=None,
        redoc_url=None,
    )

    # CORSMiddleware
    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins.split(","),
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    # Rutas
    app.include_router(autoridades)
    app.include_router(distritos)
    app.include_router(edictos)
    app.include_router(glosas)
    app.include_router(listas_de_acuerdos)
    app.include_router(materias)
    app.include_router(materias_tipos_juicios)
    app.include_router(sentencias)

    # Paginación
    add_pagination(app)

    # Mensaje de Bienvenida
    @app.get("/")
    async def root():
        """Mensaje de Bienvenida"""
        return {"message": "API para descargar archivos almacenados en depósitos que no son públicos. Hecho con FastAPI."}

    # Entregar robots.txt
    @app.get("/robots.txt", response_class=PlainTextResponse)
    async def robots():
        """robots.txt to disallow all agents"""
        return """User-agent: *\nDisallow: /"""

    # Entregar
    return app
