"""Dto declaration module."""
from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    """Base dto."""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

