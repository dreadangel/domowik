"""."""
from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from redis.asyncio.client import Redis

from app.config.data import DataSettings
from app.services.data.redis import RedisDao, create_redis


class RedisProvider(Provider):
    """Redis DI provider."""

    def __init__(self, scope: Scope = Scope.APP)-> None:
        """Ctor."""
        super().__init__(scope=scope)  # do not forget `super`

    @provide
    async def get_redis_client(self, data_config: DataSettings) -> AsyncIterable[Redis]:
        """Redis provider."""
        async with create_redis(data_config) as redis:
            yield redis

    @provide
    async def get_redis_dao(self, redis_client: Redis) -> RedisDao:
        """Redis dao provider."""
        return RedisDao(redis_client=redis_client)
