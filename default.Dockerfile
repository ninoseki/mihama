FROM python:3.11-slim-buster

WORKDIR /app

RUN apt-get update \
	&& apt-get install --no-install-recommends -y build-essential

COPY pyproject.toml poetry.lock gunicorn.conf.py requirements.txt ./

RUN pip install -U --no-cache-dir pip==23.1.2 \
	&& pip install --no-cache-dir -r requirements.txt \
	&& poetry install --without dev

COPY mihama ./mihama
