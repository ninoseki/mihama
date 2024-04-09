import contextlib
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from . import crud, deps, settings
from .api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create index
    async with deps.get_es_with_context() as es:
        await crud.index.create_if_not_exists(es, index=settings.ES_INDEX)
        await crud.index.pu_mapping(
            es, index=settings.ES_INDEX, properties={"modified": {"type": "date"}}
        )

    yield


def create_app(set_lifespan: bool = True) -> FastAPI:
    logger.add(
        settings.LOG_FILE, level=settings.LOG_LEVEL, backtrace=settings.LOG_BACKTRACE
    )

    if set_lifespan:
        app = FastAPI(
            debug=settings.DEBUG,
            title=settings.PROJECT_NAME,
            description=settings.PROJECT_DESCRIPTION,
            default_response_class=ORJSONResponse,
            lifespan=lifespan,
        )
    else:
        app = FastAPI(
            debug=settings.DEBUG,
            title=settings.PROJECT_NAME,
            description=settings.PROJECT_DESCRIPTION,
            default_response_class=ORJSONResponse,
        )

    # add middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # add routes
    app.include_router(api_router, prefix="/v1")

    with contextlib.suppress(Exception):
        app.mount("/", StaticFiles(html=True, directory="frontend/dist/"), name="index")

    return app


app = create_app()
