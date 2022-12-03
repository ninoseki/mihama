from mihama.core.datastructures import DatabaseURL

from .config import config

REDIS_OM_URL: DatabaseURL = config(
    "REDIS_OM_URL",
    cast=DatabaseURL,
    default="redis://localhost:6379",
)
REDIS_OM_BATCH_SIZE: int = config("REDIS_OM_BATCH_SIZE", cast=int, default=100)

REDIS_CACHE_URL: DatabaseURL = config(
    "REDIS_CACHE_URL",
    cast=DatabaseURL,
    default="redis://localhost:6379",
)

REDIS_CACHE_TTL: int = config(
    "REDIS_CACHE_TTL",
    cast=int,
    default=60 * 60,
)
REDIS_CACHE_NAMESPACE: str = config("REDIS_CACHE_NAMESPACE", cast=str, default="cache")
REDIS_CACHE_PREFIX: str = config(
    "REDIS_CACHE_PREFIX", cast=str, default="fastapi-cache"
)
