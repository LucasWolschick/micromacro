import urllib.parse
from httpx import AsyncClient
from pydantic import BaseModel


class ListedWarehouseModel(BaseModel):
    id: int
    description: str


class ListStocksRequest(BaseModel):
    products: list[int] | None
    warehouse_id: int | None


class ListedStockModel(BaseModel):
    product_id: int
    stock: float


ListStocksResponse = dict[int, list[ListedStockModel]]


class SetStockRequest(BaseModel):
    warehouse_id: int
    stock: float


class SetStockResponse(BaseModel):
    product_id: int
    warehouse_id: int
    stock: float


class InventoryClient:
    def __init__(self, base_url: str, client: AsyncClient):
        self.base_url = base_url
        self.client = client

    async def list_warehouses(self) -> list[ListedWarehouseModel]:
        url = urllib.parse.urljoin(self.base_url, "/stocks/warehouses")

        response = await self.client.get(url)
        response.raise_for_status()

        return [ListedWarehouseModel(**warehouse) for warehouse in response.json()]

    async def list_stocks(self, request: ListStocksRequest) -> ListStocksResponse:
        query_string = urllib.parse.urlencode(
            request.model_dump(exclude_none=True), doseq=True
        )

        url = urllib.parse.urljoin(self.base_url, f"/stocks/?{query_string}")

        response = await self.client.get(url)
        response.raise_for_status()

        print(repr(response.json()))

        return {
            id: [ListedStockModel(**stock) for stock in stocks]
            for (id, stocks) in response.json().items()
        }

    async def set_stock(
        self, product_id: int, request: SetStockRequest
    ) -> SetStockResponse:
        url = urllib.parse.urljoin(self.base_url, f"/stocks/{product_id}")

        response = await self.client.post(url, json=request.model_dump())
        print(response.json())
        response.raise_for_status()

        return SetStockResponse(**response.json())
