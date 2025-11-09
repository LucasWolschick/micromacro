from decimal import Decimal
from pydantic import BaseModel
from app.clients.catalog_client import CatalogClient
from app.clients.inventory_client import InventoryClient, ListStocksRequest


class WarehouseProductStock(BaseModel):
    warehouse: int
    quantity: Decimal


class ProductStock(BaseModel):
    total_quantity: Decimal
    deposits: list[WarehouseProductStock]


class ListedProduct(BaseModel):
    sku: int
    description: str
    price: Decimal
    stock: ProductStock


class ListProducts:
    def __init__(
        self, catalog_client: CatalogClient, inventory_client: InventoryClient
    ):
        self.catalog_client = catalog_client
        self.inventory_client = inventory_client

    async def run(self) -> list[ListedProduct]:
        products = await self.catalog_client.list_products()
        stocks = await self.inventory_client.list_stocks(
            ListStocksRequest(
                products=[product.id for product in products], warehouse_id=None
            )
        )

        stocksFromProduct: dict[int, list[WarehouseProductStock]] = {}
        totalProductStock: dict[int, Decimal] = {}

        for warehouse, productStocks in stocks.items():
            for productStock in productStocks:
                if productStock.stock.is_zero():
                    continue

                if productStock.product_id not in stocksFromProduct:
                    stocksFromProduct[productStock.product_id] = []

                if productStock.product_id not in totalProductStock:
                    totalProductStock[productStock.product_id] = Decimal("0")

                stocksFromProduct[productStock.product_id].append(
                    WarehouseProductStock(
                        warehouse=warehouse, quantity=productStock.stock
                    )
                )

                totalProductStock[productStock.product_id] += productStock.stock

        response = [
            ListedProduct(
                sku=product.id,
                description=product.description,
                price=product.price,
                stock=ProductStock(
                    total_quantity=totalProductStock.get(product.id, Decimal("0")),
                    deposits=stocksFromProduct.get(product.id, []),
                ),
            )
            for product in products
        ]

        return response
