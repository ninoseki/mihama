# frontend
FROM node:20-alpine3.18 as frontend

WORKDIR /usr/src/app

COPY ./frontend ./frontend

WORKDIR /usr/src/app/frontend

RUN npm install && npm run build && rm -rf node_modules

# base
FROM python:3.11-slim-bookworm as base

RUN apt-get update \
	&& apt-get install --no-install-recommends -y build-essential

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
	poetry install --without dev

# main
FROM python:3.11-slim-bookworm

WORKDIR /usr/src/app

COPY --from=base /usr/local/bin /usr/local/bin
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=frontend /usr/src/app/frontend ./frontend

RUN apt-get update \
	&& apt-get install --no-install-recommends -y git

COPY mihama ./mihama
COPY pyproject.toml gunicorn.conf.py ./
