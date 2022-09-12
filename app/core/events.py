from collections.abc import Callable, Coroutine
from typing import Any

import aioredis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.core import settings
from app.monkeypatch import monkeypatch_escaper
from app.redis import setup_redis_om


def create_start_app_handler(
    _: FastAPI,
) -> Callable[[], Coroutine[Any, Any, None]]:
    async def start_app() -> None:
        monkeypatch_escaper()

        await setup_redis_om()

        r = aioredis.from_url(
            str(settings.REDIS_CACHE_URL), encoding="utf8", decode_responses=True
        )
        FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")

    return start_app


def create_stop_app_handler(
    _: FastAPI,
) -> Callable[[], Coroutine[Any, Any, None]]:
    async def stop_app() -> None:
        pass

    return stop_app
