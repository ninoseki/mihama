FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get update \
	&& apt-get install --no-install-recommends -y build-essential

COPY pyproject.toml poetry.lock gunicorn.conf.py ./
COPY app ./app

RUN pip install -U --no-cache-dir pip==22.2.2 \
	&& pip install --no-cache-dir poetry==1.2.0 \
	&& poetry config virtualenvs.create false \
	&& poetry install --no-dev

EXPOSE $PORT

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]

