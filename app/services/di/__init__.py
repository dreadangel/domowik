"""DI services package."""
from dishka import STRICT_VALIDATION, AsyncContainer, make_async_container

from app.services.di.config import ConfigProvider
from app.services.di.data import RedisProvider
from app.services.di.web import HttpClientProvider


##Containers
def get_async_container_for_web() -> AsyncContainer:
    """Async container for web app."""
    return make_async_container(
        *get_providers_for_web(),
        validation_settings=STRICT_VALIDATION)

def get_async_container_for_arq_worker() -> AsyncContainer:
    """Async container for arq worker."""
    return make_async_container(
        *get_providers_for_arq_worker(),
        validation_settings=STRICT_VALIDATION)

##Providers
def get_providers_for_web() -> list:
    """DI providers list for web app."""
    return [
        ConfigProvider(),
        RedisProvider(),
        HttpClientProvider(),
    ]


def get_providers_for_arq_worker() -> list:
    """DI providers list for arq worker."""
    return [
        ConfigProvider(),
        HttpClientProvider(),
    ]

