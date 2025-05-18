"""Data process router module."""

import json
import logging

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, BackgroundTasks, UploadFile
from fastapi.exceptions import HTTPException

from app.services.data.redis import RedisDao

logger = logging.getLogger(__name__)

async def ping() -> dict:
    """."""
    return {"message": "pong"}

@inject
async def upload_file(
    redis: FromDishka[RedisDao],
    file: UploadFile,
    background_tasks: BackgroundTasks,
) -> dict:
    """File upload endpoint."""
    if file.content_type != "application/json":
        raise HTTPException(400, detail="Invalid document type")
    data = json.loads(file.file.read())
    background_tasks.add_task(
        parse_data_file,
        redis,
        data,
    )
    return {"filename": file.filename}


async def parse_data_file(redis: RedisDao, data: dict) -> None:
    """Background parsing logics."""
    for item in data:
        item_id = await redis.save_data_to_redis(item)
        # if app.state.redis
        # await app.state.redis.enqueue_job("send_email", email)

        logger.info("Item data saved succesfully: %s", item_id)

    logger.info("Data processed succesfully")


def setup() -> APIRouter:
    """Route setup method."""
    router = APIRouter(prefix="/data-process")

    router.add_api_route("/ping", ping, methods=["GET"])
    router.add_api_route(
            "/create_upload_file",
            upload_file,
            methods=["POST"],
        )

    return router

