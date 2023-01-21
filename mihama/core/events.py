from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import FastAPI

from mihama.redis import setup_redis_om


def create_start_app_handler(
    _: FastAPI,
) -> Callable[[], Coroutine[Any, Any, None]]:
    async def start_app() -> None:
        # setup Redis OM
        await setup_redis_om()

    return start_app


def create_stop_app_handler(
    _: FastAPI,
) -> Callable[[], Coroutine[Any, Any, None]]:
    async def stop_app() -> None:
        pass

    return stop_app
