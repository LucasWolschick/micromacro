from pydantic import BaseModel
from app.clients.inventory_client import InventoryClient


class ListedWarehouseResponseModel(BaseModel):
    id: int
    description: str


class ListWarehouses:
    def __init__(self, inventory_client: InventoryClient):
        self.inventory_client = inventory_client

    async def run(self):
        result = await self.inventory_client.list_warehouses()
        return [
            ListedWarehouseResponseModel(
                id=warehouse.id, description=warehouse.description
            )
            for warehouse in result
        ]
