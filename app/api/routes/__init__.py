"""Api routes module."""
from fastapi import APIRouter

from app.api.routes import data_process


def setup() -> APIRouter:
    """General routes setup method."""
    router = APIRouter()
    router.include_router(data_process.setup())

    return router

