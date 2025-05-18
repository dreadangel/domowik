"""Redis data service module."""
import json
import logging
import uuid

from redis.asyncio import Redis

from app.config.data import DataSettings, DataSourceInstanceSettings

logger = logging.getLogger(__name__)


def create_redis(config: DataSettings) -> Redis:
    """Initiate Redis connection."""
    logger.info("created redis for %s", config)
    redis_config:DataSourceInstanceSettings = config.get_settings("redis")
    return Redis(host=redis_config.host, port=redis_config.port, db=0)


class RedisDao:
    """Redis related data management."""

    def __init__(self, redis_client:Redis) -> None:
        """Ctor."""
        self.client = redis_client

    async def save_data_to_redis(self, data: dict) ->uuid.UUID:
        """Save data to Redis."""
        data_id = uuid.uuid4()
        await self.client.set(str(data_id), json.dumps(data))
        return data_id

