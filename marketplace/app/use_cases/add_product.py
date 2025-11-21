from pydantic import BaseModel
from app.clients import catalog_client
from app.clients.catalog_client import CatalogClient


class AddProductRequest(BaseModel):
    description: str
    price: float


class AddProductResponse(BaseModel):
    id: int
    description: str
    price: float
    vendor_id: int


class AddProduct:
    def __init__(self, catalog_client: CatalogClient):
        self.catalog_client = catalog_client

    async def run(self, token: str, request: AddProductRequest):
        result = await self.catalog_client.add_product(
            token,
            catalog_client.AddProductRequest(
                description=request.description, price=request.price
            ),
        )
        return AddProductResponse(
            id=result.id,
            description=result.description,
            price=result.price,
            vendor_id=result.vendor_id,
        )
