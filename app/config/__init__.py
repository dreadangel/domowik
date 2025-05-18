"""Application config root package."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config.app import AppSettings
from app.config.data import DataSettings
from app.config.http import HttpSettings


class Settings(BaseSettings):
    """Application settings."""

    app: AppSettings = AppSettings()
    http: HttpSettings = HttpSettings()
    data: DataSettings = DataSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="allow",
        env_nested_delimiter=".",
        frozen=True,
    )


@lru_cache
def get_settings() -> Settings:
    """Get app settings."""
    setting: Settings = Settings()
    return setting
