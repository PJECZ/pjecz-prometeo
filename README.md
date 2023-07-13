# pjecz-prometeo

Entregar archivos almacenados en depósitos que no son públicos. Hecho con FastAPI.

## Mejores practicas

Usa las recomendaciones de [I've been abusing HTTP Status Codes in my APIs for years](https://blog.slimjim.xyz/posts/stop-using-http-codes/)

### Respuesta exitosa

Status code: **200**

Body que entrega un listado

    {
        "success": true,
        "message": "Success",
        "total": 2812,
        "items": [
            {
                "id": 123,
                ...
            },
            ...
        ],
        "limit": 100,
        "offset": 0
    }

Body que entrega un item

    {
        "success": true,
        "message": "Success",
        "id": 123,
        ...
    }

### Respuesta fallida: registro no encontrado

Status code: **200**

Body

    {
        "success": false,
        "message": "No employee found for ID 100"
    }

### Respuesta fallida: ruta incorrecta

Status code: **404**

## Configure Poetry

Por defecto, con **poetry** el entorno se guarda en un directorio en `~/.cache/pypoetry/virtualenvs`

Modifique para que el entorno se guarde en el mismo directorio que el proyecto

    poetry config --list
    poetry config virtualenvs.in-project true

Verifique que este en True

    poetry config virtualenvs.in-project

## Configuracion

**Para desarrollo** hay que crear un archivo para las variables de entorno `.env`

    # Base de datos
    DB_HOST=127.0.0.1
    DB_PORT=5432
    DB_NAME=pjecz_plataforma_web
    DB_USER=readerpjeczplataformaweb
    DB_PASS=XXXXXXXXXXXXXXXX

    # Fernet key para cifrar y descifrar la API_KEY
    FERNET_KEY="XXXXXXXXXXXXXXXX"

    # CORS origins
    ORIGINS=http://localhost:3000,http://localhost:5000,http://127.0.0.1:3000,http://127.0.0.1:5000

    # Huso horario
    TZ=America/Mexico_City

    # Username es una dirección de correo electrónico para identificar al cliente
    USERNAME=anonymous@server.net

Cree un archivo `.bashrc` que se puede usar en el perfil de **Konsole**

    if [ -f ~/.bashrc ]
    then
        . ~/.bashrc
    fi

    if command -v figlet &> /dev/null
    then
        figlet Prometeo
    else
        echo "== Prometeo"
    fi
    echo

    if [ -f .env ]
    then
        export $(grep -v '^#' .env | xargs)
        echo "-- Variables de entorno"
        echo "   DB_HOST: ${DB_HOST}"
        echo "   DB_PORT: ${DB_PORT}"
        echo "   DB_NAME: ${DB_NAME}"
        echo "   DB_USER: ${DB_USER}"
        echo "   DB_PASS: ${DB_PASS}"
        echo "   ORIGINS: ${ORIGINS}"
        echo "   TZ: ${TZ}"
        echo
        export PGHOST=$DB_HOST
        export PGPORT=$DB_PORT
        export PGDATABASE=$DB_NAME
        export PGUSER=$DB_USER
        export PGPASSWORD=$DB_PASS
    fi

    if [ -d .venv ]
    then
        source .venv/bin/activate
        export PYTHONPATH=$(pwd)
        echo "-- Python Virtual Environment"
        echo "   $(python3 --version)"
        echo "   PYTHONPATH: ${PYTHONPATH}"
        echo
        alias arrancar="uvicorn --factory --host=127.0.0.1 --port 8004 --reload prometeo.app:create_app"
        echo "-- Ejecutar FastAPI 127.0.0.1:8004"
        echo "   arrancar"
        echo
    fi

    if [ -d tests ]
    then
        echo "-- Pruebas unitarias"
        echo "   python -m unittest discover tests"
        echo
    fi

    if [ -f .github/workflows/gcloud-app-deploy.yml ]
    then
        echo "-- Google Cloud"
        echo "   GitHub Actions hace el deploy en Google Cloud"
        echo "   Si hace cambios en pyproject.toml reconstruya requirements.txt"
        echo "   poetry export -f requirements.txt --output requirements.txt --without-hashes"
        echo
    fi

## Instalacion

En Fedora Linux agregue este software

    sudo dnf -y groupinstall "Development Tools"
    sudo dnf -y install glibc-langpack-en glibc-langpack-es
    sudo dnf -y install pipenv poetry python3-virtualenv
    sudo dnf -y install python3-devel python3-docs python3-idle
    sudo dnf -y install python3.11

Clone el repositorio

    cd ~/Documents/GitHub/PJECZ
    git clone https://github.com/PJECZ/pjecz-prometeo.git
    cd pjecz-prometeo

Instale el entorno virtual con **Python 3.11** y los paquetes necesarios

    python3.11 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install wheel
    poetry install

## Arrancar para desarrollo

Ejecute `arrancar` que es un alias dentro de `.bashrc`

    arrancar

## Pruebas

Para ejecutar las pruebas arranque el servidor y ejecute

    python -m unittest discover tests

## Contenedores

Esta incluido el archivo `Dockerfile` para construir la imagen

Va a usar el puerto **8000** para la API

Construir la imagen con el comando **podman**

    podman build -t pjecz_prometeo .

Escribir el archivo `.env` con las variables de entorno

    DB_HOST=NNN.NNN.NNN.NNN
    DB_PORT=5432
    DB_NAME=pjecz_plataforma_web
    DB_USER=readerpjeczplataformaweb
    DB_PASS=XXXXXXXXXXXXXXXX
    FERNET_KEY="XXXXXXXXXXXXXXXX"
    ORIGINS=*
    USERNAME=anonymous@server.net

Arrancar el contenedor donde el puerto 8000 del contendor se dirige al puerto 7001 local

    podman run --rm \
        --name pjecz_prometeo \
        -p 7001:8000 \
        --env-file .env \
        pjecz_prometeo

Arrancar el contenedor y dejar corriendo en el fondo

    podman run -d \
        --name pjecz_prometeo \
        -p 7001:8000 \
        --env-file .env \
        pjecz_prometeo

Detener contenedor

    podman container stop pjecz_prometeo

Arrancar contenedor

    podman container start pjecz_prometeo

Eliminar contenedor

    podman container rm pjecz_prometeo

Eliminar la imagen

    podman image rm pjecz_prometeo

## Google Cloud deployment

Este proyecto usa **GitHub Actions** para subir a **Google Cloud**

Y se toman las variables de entorno desde **Google Cloud** con _secret manager_

En caso de haber cambiado las dependencias se debe sobrescribir el archivo `requirements.txt`

    poetry export -f requirements.txt --output requirements.txt --without-hashes
