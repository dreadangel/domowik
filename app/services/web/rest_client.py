"""Http client module."""

import logging
from abc import abstractmethod
from http import HTTPMethod
from typing import Protocol

import httpx

from app.config.http import HttpServiceSettings, HttpSettings

logger = logging.getLogger(__name__)

class HttpClient(Protocol):
    """Base Http client class."""

    @abstractmethod
    def do_request(self) -> None:
        """Abstract request method."""
        raise NotImplementedError



class BeeceptorHttpClient(HttpClient):
    """Beecepter http client."""

    def __init__(self, http_config: HttpSettings) -> None:
        """Ctor."""
        self.config = http_config

    async def do_request(self) -> None:
        """Beeceptor http client."""
        service_config:HttpServiceSettings = self.config.get_settings("beeceptor")
        headers = {"Accept": "*/*"}
        async with httpx.AsyncClient(timeout=service_config.timeout) as client:
            data = await client.send(httpx.Request(method=HTTPMethod.GET, url=service_config.api_url, headers=headers))
            logger.info("Service %s returned: %s ",service_config.api_url, str(data))



class AzureFnHttpClient(HttpClient):
    """Azure function http client."""

    def __init__(self, http_config: HttpSettings) -> None:
        """Ctor."""
        self.config = http_config

    async def do_request(self, name:str = "user") -> None:
        """Beeceptor http client."""
        service_config:HttpServiceSettings = self.config.get_settings("azure_fn")
        headers = {"Accept": "*/*"}
        async with httpx.AsyncClient(timeout=service_config.timeout) as client:
            url:str = f"{service_config.api_url}/{name}"
            data = await client.send(httpx.Request(method=HTTPMethod.GET, url=url, headers=headers))
            logger.info("Service %s returned: %s ",service_config.api_url, str(data))
