from pydantic import BaseModel
from app.clients.inventory_client import InventoryClient, ListStocksRequest


class ProductQuote(BaseModel):
    warehouse_id: int
    quantity: float


class GetProductAvailabilityRequest(BaseModel):
    product_id: int
    quantity_requested: float


class GetProductAvailabilityResponse(BaseModel):
    product_id: int
    quantity_requested: float
    available: bool
    quotes: list[ProductQuote]


class GetProductAvailability:
    def __init__(self, inventory_client: InventoryClient):
        self.inventory_client = inventory_client

    async def run(self, product: GetProductAvailabilityRequest):
        stocks = await self.inventory_client.list_stocks(
            ListStocksRequest(products=[product.product_id], warehouse_id=None)
        )

        all_quotes = (
            ProductQuote(
                warehouse_id=warehouse_id,
                quantity=next(
                    s.stock for s in stock if s.product_id == product.product_id
                ),
            )
            for warehouse_id, stock in stocks.items()
            if len(stock) > 0
        )

        quotes = [
            quote for quote in all_quotes if quote.quantity > product.quantity_requested
        ]

        available = len(quotes) > 0

        return GetProductAvailabilityResponse(
            product_id=product.product_id,
            quantity_requested=product.quantity_requested,
            available=available,
            quotes=quotes,
        )
