"""DB configuration dto."""

from pydantic import BaseModel, Field


class DataSourceInstanceSettings(BaseModel):
    """A data source settings."""

    host: str = Field(default="127.0.0.1")
    port: int = Field(default="0")
    db_name: str = Field(default="")
    user_name: str = Field(default="")
    password: str = Field(default="")


class DataSettings(BaseModel):
    """Data settings."""

    data_source: dict[str, DataSourceInstanceSettings] = {}

    def get_settings(self, service_name:str)-> DataSourceInstanceSettings:
        """Find a data source settings if any."""
        if service_name not in self.data_source:
            msg = f"Could not found settings for data source {service_name}"
            raise KeyError(msg)
        return self.data_source[service_name]

