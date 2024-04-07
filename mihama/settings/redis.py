from arq import constants
from arq.connections import RedisSettings
from starlette.datastructures import CommaSeparatedStrings

from mihama.datastructures import DatabaseURL
from mihama.utils import cast_csv

from .config import config

REDIS_URL: DatabaseURL = config(
    "REDIS_URL",
    cast=DatabaseURL,
    default="redis://localhost:6379",
)
REDIS_CONN_TIMEOUT: int = config("REDIS_CONN_TIMEOUT", cast=int, default=10)
REDIS_CONN_RETRIES: int = config("REDIS_CONN_RETRIES", cast=int, default=5)
REDIS_CONN_RETRY_DELAY: int = config("REDIS_CONN_RETRY_DELAY", cast=int, default=1)

REDIS_SETTINGS = RedisSettings(
    host=REDIS_URL.hostname or "localhost",
    port=REDIS_URL.port or 6379,
    password=REDIS_URL.password,
    conn_retries=REDIS_CONN_RETRIES,
    conn_timeout=REDIS_CONN_TIMEOUT,
    conn_retry_delay=REDIS_CONN_RETRY_DELAY,
)

ARQ_DEFAULT_QUEUE_NAME: str = config(
    "ARQ_DEFAULT_QUEUE_NAME", cast=str, default=constants.default_queue_name
)
ARQ_CRON_JOBS_RUN_AT_START_UP: bool = config(
    "ARQ_CRON_JOBS_RUN_AT_START_UP", cast=bool, default=True
)
ARQ_CRON_JOBS_HOUR = set(
    cast_csv(
        config("ARQ_CRON_JOBS_HOUR", cast=CommaSeparatedStrings, default="0"), cast=int
    )
)
ARQ_CRON_JOBS_MINUTE = set(
    cast_csv(
        config("ARQ_CRON_JOBS_MINUTE", cast=CommaSeparatedStrings, default="0"),
        cast=int,
    )
)
