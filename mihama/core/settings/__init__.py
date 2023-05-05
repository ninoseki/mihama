import sys

from .arq import (  # noqa:F401
    ARQ_CRON_JOBS_HOUR_INT_SET,
    ARQ_CRON_JOBS_MINUTE_INT_SET,
    ARQ_CRON_JOBS_RUN_AT_START_UP,
    ARQ_DEFAULT_QUEUE_NAME,
    ARQ_REDIS_SETTINGS,
)
from .config import config
from .osv import (  # noqa: F401
    OSV_BUCKET_BASE_URL,
    OSV_BUCKET_TIMEOUT,
    OSV_ECOSYSTEMS,
    OSV_QUERY_BATCH_MAX_AT_ONCE,
)
from .redis import (  # noqa: F401
    REDIS_CACHE_NAMESPACE,
    REDIS_CACHE_PREFIX,
    REDIS_CACHE_TTL,
    REDIS_CACHE_URL,
    REDIS_OM_BATCH_SIZE,
    REDIS_OM_URL,
)

PROJECT_NAME: str = config("PROJECT_NAME", default="mihama")
PROJECT_DESCRIPTION: str = config("PROJECT_DESCRIPTION", default="osv.dev API clone")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
TESTING: bool = config("TESTING", cast=bool, default=False)

LOG_FILE = config("LOG_FILE", default=sys.stderr)
LOG_LEVEL: str = config("LOG_LEVEL", cast=str, default="DEBUG")
LOG_BACKTRACE: bool = config("LOG_BACKTRACE", cast=bool, default=True)
