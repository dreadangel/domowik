"""Application start module."""

import asyncio
import contextlib

import uvicorn
from fastapi import FastAPI
from typer import Typer

from app import init_web_app, setup_arq_worker, setup_logging
from app.config import Settings, get_settings

cli_application = Typer()


@cli_application.command()
def web() -> None:
    """Web application start."""
    settings:Settings = get_settings()
    app:FastAPI = init_web_app()

    uvicorn.run(
        app=app,
        host=settings.app.host,
        port=settings.app.port,
        log_config=None,
    )


async def run_arq_worker()-> None:
    """Arq worker run."""
    worker, container = setup_arq_worker()

    try:
        await worker.async_run()
    finally:
        await container.close()
        await worker.close()


@cli_application.command()
def arq() -> None:
    """Arq worker start."""
    with contextlib.suppress(asyncio.CancelledError):
        asyncio.run(run_arq_worker())


if __name__ == "__main__":
    setup_logging()
    cli_application()
