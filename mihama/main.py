from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from loguru import logger

from .api.v1.api import api_router
from .core import settings
from .core.events import create_start_app_handler, create_stop_app_handler
from .views import view_router


def create_app(add_event_handlers: bool = True) -> FastAPI:
    logger.add(
        settings.LOG_FILE, level=settings.LOG_LEVEL, backtrace=settings.LOG_BACKTRACE
    )

    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        default_response_class=ORJSONResponse,
    )

    # add middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # add event handlers
    if add_event_handlers:
        app.add_event_handler("startup", create_start_app_handler(app))
        app.add_event_handler("shutdown", create_stop_app_handler(app))

    # add routes
    app.include_router(view_router)
    app.include_router(api_router, prefix="/v1")

    return app


app = create_app()
