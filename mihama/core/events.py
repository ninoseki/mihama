from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from mihama.core import settings
from mihama.redis import setup_redis_om


def create_start_app_handler(
    _: FastAPI,
) -> Callable[[], Coroutine[Any, Any, None]]:
    async def start_app() -> None:
        # setup Redis OM
        await setup_redis_om()

        # setup cache
        r = aioredis.from_url(str(settings.REDIS_CACHE_URL))
        FastAPICache.init(RedisBackend(r), prefix=settings.REDIS_CACHE_PREFIX)

    return start_app


def create_stop_app_handler(
    _: FastAPI,
) -> Callable[[], Coroutine[Any, Any, None]]:
    async def stop_app() -> None:
        pass

    return stop_app
