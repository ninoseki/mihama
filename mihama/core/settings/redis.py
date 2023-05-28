from mihama.core.datastructures import DatabaseURL

from .config import config

REDIS_OM_URL: DatabaseURL = config(
    "REDIS_OM_URL",
    cast=DatabaseURL,
    default="redis://localhost:6379",
)
REDIS_OM_BATCH_SIZE: int = config("REDIS_OM_BATCH_SIZE", cast=int, default=100)
