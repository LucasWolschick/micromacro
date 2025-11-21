from pydantic import BaseModel
from app.clients.catalog_client import CatalogClient
from app.clients.inventory_client import InventoryClient, SetStockRequest


class UpdateStockRequest(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: float


class UpdateStockResponse(UpdateStockRequest):
    pass


class UpdateStock:
    def __init__(
        self, catalog_client: CatalogClient, inventory_client: InventoryClient
    ):
        self.catalog_client = catalog_client
        self.inventory_client = inventory_client

    async def run(self, request: UpdateStockRequest, token: str):
        _ = await self.catalog_client.get_product(request.product_id)

        response = await self.inventory_client.set_stock(
            request.product_id,
            token,
            SetStockRequest(
                warehouse_id=request.warehouse_id,
                stock=request.quantity,
            ),
        )

        return UpdateStockResponse(
            product_id=response.product_id,
            warehouse_id=response.warehouse_id,
            quantity=response.stock,
        )
