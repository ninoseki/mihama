FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get update \
	&& apt-get install --no-install-recommends -y build-essential

COPY pyproject.toml poetry.lock gunicorn.conf.py requirements.txt ./

RUN pip install -U --no-cache-dir pip==22.3.1 \
	&& pip install --no-cache-dir -r requirements.txt \
	&& poetry install --without dev

COPY mihama ./mihama

EXPOSE $PORT
