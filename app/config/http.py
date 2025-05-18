"""HTTP clients configuration dto."""

from enum import StrEnum

from pydantic import BaseModel, Field


class ServiceType(StrEnum):
    """HTTP clients codes."""

    BEECEPTOR = "beeceptor"


class HttpServiceSettings(BaseModel):
    """Http service settings."""

    protocol: str = Field(default="http")
    host: str = Field(default="127.0.0.1")
    api_root: str = Field(default="")
    timeout: int = Field(default=10)

    @property
    def api_url(self)->str:
        """Http service url."""
        return f"{self.protocol}://{self.host}{self.api_root}"


class HttpSettings(BaseModel):
    """HTTP settings."""

    services: dict[str, HttpServiceSettings] = {}

    def get_settings(self, service_name:str)-> HttpServiceSettings:
        """Find http service setting if any."""
        if service_name not in self.services:
            msg = f"Could not found settings for service {service_name}"
            raise KeyError(msg)
        return self.services[service_name]

