from pydantic import BaseModel
from app.clients import inventory_client
from app.clients.inventory_client import InventoryClient


class AddWarehouseRequest(BaseModel):
    description: str


class AddWarehouseResponse(BaseModel):
    id: int
    description: str


class AddWarehouse:
    def __init__(self, inventory_client: InventoryClient):
        self.inventory_client = inventory_client

    async def run(self, token: str, request: AddWarehouseRequest):
        result = await self.inventory_client.add_warehouse(
            token, inventory_client.AddWarehouseRequest(description=request.description)
        )
        return result
