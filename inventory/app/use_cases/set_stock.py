from pydantic import BaseModel

from app.repositories.stock_repository import StockRepository
from app.core.stock import Stock
from app.exceptions import WarehouseNotFoundException
from app.repositories.warehouse_repository import WarehouseRepository


class SetStockRequest(BaseModel):
    product_id: int
    warehouse_id: int
    stock: float = 0.0


class SetStockResponse(BaseModel):
    product_id: int
    warehouse_id: int
    stock: float


class SetStock:
    def __init__(
        self,
        stock_repository: StockRepository,
        warehouse_repository: WarehouseRepository,
    ):
        self.stock_repository = stock_repository
        self.warehouse_repository = warehouse_repository

    async def run(self, request: SetStockRequest) -> SetStockResponse:
        if not await self.warehouse_repository.exists(request.warehouse_id):
            raise WarehouseNotFoundException(request.warehouse_id)

        p = Stock(
            id=0,
            product_id=request.product_id,
            warehouse_id=request.warehouse_id,
            stock=request.stock,
        )

        r = await self.stock_repository.set(p)

        return SetStockResponse(
            product_id=r.product_id, warehouse_id=r.warehouse_id, stock=r.stock
        )
