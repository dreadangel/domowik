"""Long task management with arq module."""

import logging
from typing import Any

from arq.connections import RedisSettings
from dishka import FromDishka
from dishka.integrations.arq import inject

from app.services.web.rest_client import AzureFnHttpClient

logger = logging.getLogger(__name__)
REDIS_SETTINGS = RedisSettings()


@inject
async def do_fn_request(
    _: dict[Any, Any],
    name:str,
    rest_client: FromDishka[AzureFnHttpClient],
) -> None:
    """Job function."""
    result = await rest_client.do_request(name=name)
    logger.info(result)


async def startup(ctx: dict[Any, Any])-> None:
    """."""
    logger.info("Arq worker started.")


async def shutdown(ctx: dict[Any, Any])-> None:
    """."""
    logger.info("Arq worker shutdown.")


class WorkerSettings:
    """Worker for arq job execution."""

    functions = [do_fn_request]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = REDIS_SETTINGS


