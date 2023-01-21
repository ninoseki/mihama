from aiocache import Cache, decorators
from aiocache.serializers import PickleSerializer

from mihama.core import settings
from mihama.core.datastructures import DatabaseURL

from .key_builder import default_key_builder

cache = Cache.REDIS

if settings.TESTING:
    cache = Cache.MEMORY


class cached(decorators.cached):
    def __init__(
        self,
        ttl=settings.REDIS_CACHE_TTL,
        key_builder=default_key_builder,
        cache=cache,
        serializer=PickleSerializer(),
        plugins=None,
        alias=None,
        noself=False,
        namespace: str = settings.REDIS_CACHE_NAMESPACE,
        redis_url: DatabaseURL = settings.REDIS_CACHE_URL,
        **kwargs,
    ):
        super().__init__(
            ttl=ttl,
            key=None,
            key_builder=key_builder,
            noself=noself,
            alias=alias,
            cache=cache,
            serializer=serializer,
            plugins=plugins,
            namespace=namespace,
            endpoint=redis_url.hostname,
            port=redis_url.port,
            password=redis_url.password,
            **kwargs,
        )
