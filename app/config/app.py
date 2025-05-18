"""Application configuration dto."""

from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    """Web application startup settings."""

    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)
