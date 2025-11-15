from pydantic import BaseModel
from app.clients.catalog_client import CatalogClient
from app.clients.inventory_client import InventoryClient, ListStocksRequest


class WarehouseProductStock(BaseModel):
    warehouse: int
    quantity: float


class ProductStock(BaseModel):
    total_quantity: float
    deposits: list[WarehouseProductStock]


class GetProductResponse(BaseModel):
    sku: int
    description: str
    price: float
    stock: ProductStock


class GetProduct:
    def __init__(
        self, catalog_client: CatalogClient, inventory_client: InventoryClient
    ):
        self.catalog_client = catalog_client
        self.inventory_client = inventory_client

    async def run(self, product_id: int) -> GetProductResponse:
        product = await self.catalog_client.get_product(product_id)
        stocks = await self.inventory_client.list_stocks(
            ListStocksRequest(products=[product_id], warehouse_id=None)
        )

        stocksFromProduct: dict[int, list[WarehouseProductStock]] = {}
        totalProductStock: dict[int, float] = {}

        for warehouse, productStocks in stocks.items():
            for productStock in productStocks:
                if productStock.stock.is_zero():
                    continue

                if productStock.product_id not in stocksFromProduct:
                    stocksFromProduct[productStock.product_id] = []

                if productStock.product_id not in totalProductStock:
                    totalProductStock[productStock.product_id] = 0.0

                stocksFromProduct[productStock.product_id].append(
                    WarehouseProductStock(
                        warehouse=warehouse, quantity=productStock.stock
                    )
                )

                totalProductStock[productStock.product_id] += productStock.stock

        response = GetProductResponse(
            sku=product.id,
            description=product.description,
            price=product.price,
            stock=ProductStock(
                total_quantity=totalProductStock.get(product.id, 0.0),
                deposits=stocksFromProduct.get(product.id, []),
            ),
        )

        return response
