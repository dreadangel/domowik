"""."""

from dishka import Provider, Scope, provide

from app.config.http import HttpSettings
from app.services.web.rest_client import AzureFnHttpClient, BeeceptorHttpClient


class HttpClientProvider(Provider):
    """Http clients DI provider."""

    def __init__(self, scope: Scope = Scope.APP)-> None:
        """Ctor."""
        super().__init__(scope=scope)  # do not forget `super`

    @provide
    async def get_beeceptor_client(self, settings: HttpSettings) -> BeeceptorHttpClient:
        """Beeceptor client provider."""
        return BeeceptorHttpClient(http_config=settings)

    @provide
    async def get_azure_fn_client(self, settings: HttpSettings) -> AzureFnHttpClient:
        """Azure function client provider."""
        return AzureFnHttpClient(http_config=settings)
