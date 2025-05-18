"""Root application module."""
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import yaml
from arq.worker import Worker, create_worker
from dishka import AsyncContainer, plotter
from dishka.integrations.arq import setup_dishka as arq_setup_dishka
from dishka.integrations.fastapi import setup_dishka as fastapi_setup_dishka
from fastapi import FastAPI

from app.api import routes
from app.services import di
from app.services.queues import arq_service

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    """Lifespan for proper dishca shutdown."""
    yield

    if app.state.dishka_container:
        await app.state.dishka_container.close()


def init_web_app() -> FastAPI:
    """Web application initialization."""
    app = FastAPI(lifespan=lifespan)
    app.include_router(routes.setup())

    container = di.get_async_container_for_web()
    fastapi_setup_dishka(container, app)
    logger.info(
        "app prepared with dishka:\n%s",
        plotter.render_mermaid(container),
    )
    return app


def setup_arq_worker() -> tuple[Worker, AsyncContainer]:
    """Arq worker initialization."""
    worker: Worker = create_worker(arq_service.WorkerSettings)

    container:AsyncContainer = di.get_async_container_for_arq_worker()
    arq_setup_dishka(container=container, worker_settings=worker)

    return worker, container


def setup_logging()->None:
    """Logger configuration setup."""
    try:
        with Path("logging.yml").open("r") as f:
            logging_config = yaml.safe_load(f)
        logging.config.dictConfig(logging_config)
        logger.info("Logging configured successfully")
    except OSError:
        logging.basicConfig(level=logging.DEBUG)
        logger.warning("logging config file not found, use basic config")
