import sys

from .config import config
from .es import ES_HOSTS, ES_INDEX, ES_PASSWORD, ES_USERNAME  # noqa: F401
from .ossf import (  # noqa: F401
    ENABLE_OSSF_MALICIOUS_PACKAGES,
    OSSF_MALICIOUS_PACKAGES_REPO_URL,
)
from .osv import (  # noqa: F401
    OSV_BUCKET_BASE_URL,
    OSV_BUCKET_TIMEOUT,
    OSV_ECOSYSTEMS,
)
from .redis import (  # noqa:F401
    ARQ_CRON_JOBS_HOUR,
    ARQ_CRON_JOBS_MINUTE,
    ARQ_CRON_JOBS_RUN_AT_START_UP,
    ARQ_DEFAULT_QUEUE_NAME,
    REDIS_SETTINGS,
)

PROJECT_NAME: str = config("PROJECT_NAME", default="mihama")
PROJECT_DESCRIPTION: str = config("PROJECT_DESCRIPTION", default="osv.dev API clone")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
TESTING: bool = config("TESTING", cast=bool, default=False)

LOG_FILE = config("LOG_FILE", default=sys.stderr)  # type: ignore
LOG_LEVEL: str = config("LOG_LEVEL", cast=str, default="DEBUG")
LOG_BACKTRACE: bool = config("LOG_BACKTRACE", cast=bool, default=True)
