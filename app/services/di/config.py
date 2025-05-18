
"""."""

from dishka import Provider, Scope, provide

from app.config import Settings, get_settings
from app.config.data import DataSettings
from app.config.http import HttpSettings


class ConfigProvider(Provider):
    """Config DI provider."""

    def __init__(self, scope: Scope = Scope.APP)-> None:
        """Ctor."""
        super().__init__(scope=scope)

    @provide
    def data_global_config(self) -> Settings:
        """Global config provider."""
        return get_settings()

    @provide
    def data_config(self, settings:Settings) -> DataSettings:
        """Data sources config provider."""  # noqa: D401
        return settings.data

    @provide
    def http_config(self, settings:Settings) -> HttpSettings:
        """Http clients config provider."""
        return settings.http
