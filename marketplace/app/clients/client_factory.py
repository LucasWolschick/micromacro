from httpx import AsyncClient

from app.settings import settings

from .inventory_client import InventoryClient
from .catalog_client import CatalogClient


class ClientFactory:
    def __init__(self, client: AsyncClient):
        self.client = client

    def catalog(self):
        if not hasattr(self, "catalog_client"):
            self.catalog_client = CatalogClient(
                settings.catalog_api_url.encoded_string(), self.client
            )

        return self.catalog_client

    def inventory(self):
        if not hasattr(self, "inventory_client"):
            self.inventory_client = InventoryClient(
                settings.inventory_api_url.encoded_string(), self.client
            )

        return self.inventory_client
