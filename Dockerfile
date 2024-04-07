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

RUN apt-get update \
	&& apt-get install --no-install-recommends -y git

COPY mihama ./mihama
COPY pyproject.toml gunicorn.conf.py ./
