from collections.abc import Callable

from fastapi_cache import FastAPICache
from fastapi_cache.coder import Coder
from fastapi_cache.decorator import cache as _cache

from app.core import settings


def cache(
    expire: int = settings.REDIS_CACHE_TTL,
    coder: type[Coder] = FastAPICache.get_coder(),
    key_builder: Callable = FastAPICache.get_key_builder(),
    namespace: str = settings.REDIS_CACHE_NAMESPACE,
):
    return _cache(expire, coder, key_builder, namespace)
