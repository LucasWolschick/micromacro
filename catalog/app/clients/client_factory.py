from httpx import AsyncClient

from app.settings import settings

from .vendors_client import VendorsClient


class ClientFactory:
    def __init__(self, client: AsyncClient):
        self.client = client

    def vendors(self):
        if not hasattr(self, "vendors_client"):
            self.vendors_client = VendorsClient(
                settings.vendors_api_url.encoded_string(), self.client
            )

        return self.vendors_client
