from collections.abc import Sequence
from typing import Any

from arq.connections import RedisSettings
from arq.cron import CronJob, cron
from arq.typing import StartupShutdown, WorkerCoroutine
from arq.worker import Function, func

from mihama.core import settings
from mihama.redis import setup_redis_om

from . import constants, tasks


async def startup(_: dict[Any, Any]) -> None:
    # setup Redis OM
    await setup_redis_om()


async def shutdown(_: dict[Any, Any]) -> None:
    pass


class ArqWorkerSettings:
    redis_settings: RedisSettings = settings.ARQ_REDIS_SETTINGS

    queue_name: str = settings.ARQ_DEFAULT_QUEUE_NAME

    on_startup: StartupShutdown | None = startup  # type: ignore
    on_shutdown: StartupShutdown | None = shutdown  # type: ignore

    functions: Sequence[Function | WorkerCoroutine] = [
        func(
            tasks.update_by_ecosystem_task,  # type: ignore
            name=constants.UPDATE_BY_ECOSYSTEM_TASK,
        ),
    ]

    cron_jobs: Sequence[CronJob] | None = [
        cron(
            tasks.update_by_ecosystems_task,  # type: ignore
            name=constants.UPDATE_BY_ECOSYSTEMS_TASK,
            hour=settings.ARQ_CRON_JOBS_HOUR_INT_SET,
            minute=settings.ARQ_CRON_JOBS_MINUTE_INT_SET,
            run_at_startup=settings.ARQ_CRON_JOBS_RUN_AT_START_UP,
        )
    ]
