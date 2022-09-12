from arq import constants
from arq.connections import RedisSettings
from starlette.datastructures import CommaSeparatedStrings

from app.core.datastructures import DatabaseURL

from .config import config

ARQ_REDIS_URL: DatabaseURL = config(
    "ARQ_REDIS_URL",
    cast=DatabaseURL,
    default="redis://localhost:6379",
)
ARQ_REDIS_CONN_TIMEOUT: int = config("ARQ_REDIS_CONN_TIMEOUT", cast=int, default=10)
ARQ_REDIS_CONN_RETRIES: int = config("ARQ_REDIS_CONN_RETRIES", cast=int, default=5)
ARQ_REDIS_CONN_RETRY_DELAY: int = config(
    "ARQ_REDIS_CONN_RETRY_DELAY", cast=int, default=1
)
ARQ_DEFAULT_QUEUE_NAME: str = config(
    "ARQ_DEFAULT_QUEUE_NAME", cast=str, default=constants.default_queue_name
)

ARQ_REDIS_SETTINGS = RedisSettings(
    host=ARQ_REDIS_URL.hostname or "localhost",
    port=ARQ_REDIS_URL.port or 6379,
    password=ARQ_REDIS_URL.password,
    conn_retries=ARQ_REDIS_CONN_RETRIES,
    conn_timeout=ARQ_REDIS_CONN_TIMEOUT,
    conn_retry_delay=ARQ_REDIS_CONN_RETRY_DELAY,
)


ARQ_CRON_JOBS_RUN_AT_START_UP: bool = config(
    "ARQ_CRON_JOBS_RUN_AT_START_UP", cast=bool, default=True
)
ARQ_CRON_JOBS_HOUR: CommaSeparatedStrings = config(
    "ARQ_CRON_JOBS_HOUR", cast=CommaSeparatedStrings, default="0"
)
ARQ_CRON_JOBS_MINUTE: CommaSeparatedStrings = config(
    "ARQ_CRON_JOBS_MINUTE", cast=CommaSeparatedStrings, default="0"
)

ARQ_CRON_JOBS_HOUR_INT_SET: set[int] = {int(h) for h in ARQ_CRON_JOBS_HOUR}
ARQ_CRON_JOBS_MINUTE_INT_SET: set[int] = {int(h) for h in ARQ_CRON_JOBS_MINUTE}
