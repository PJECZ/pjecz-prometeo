FROM python:3.11

WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8004

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:8004", "-k", "uvicorn.workers.UvicornWorker", "prometeo.app:create_app" ]
