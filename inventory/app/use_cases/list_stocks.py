from pydantic import BaseModel

from app.repositories.stock_repository import StockRepository
from app.repositories.warehouse_repository import WarehouseRepository
from app.core.warehouse import Warehouse
from app.exceptions import WarehouseNotFoundException


class ListStocksRequest(BaseModel):
    products: list[int] | None
    warehouse_id: int | None


class ListedStockModel(BaseModel):
    product_id: int
    stock: float


ListStocksResponse = dict[int, list[ListedStockModel]]


class ListStocks:
    def __init__(
        self,
        stock_repository: StockRepository,
        warehouse_repository: WarehouseRepository,
    ):
        self.stock_repository = stock_repository
        self.warehouse_repository = warehouse_repository

    async def run(self, request: ListStocksRequest) -> ListStocksResponse:
        if request.warehouse_id is None:
            stocks = await self.stock_repository.list()
            warehouses = await self.warehouse_repository.list()
        else:
            if not await self.warehouse_repository.exists(request.warehouse_id):
                raise WarehouseNotFoundException(request.warehouse_id)

            stocks = await self.stock_repository.list_from_warehouse(
                request.warehouse_id
            )
            warehouses = [Warehouse(id=request.warehouse_id, description="")]

        product_set: set[int]
        if request.products:
            product_set = set(request.products)
        else:
            product_set = set()

        products_per_warehouse = {
            warehouse.id: [
                ListedStockModel(product_id=stock.product_id, stock=stock.stock)
                for stock in stocks
                if stock.warehouse_id == warehouse.id
                and (not product_set or stock.product_id in product_set)
            ]
            for warehouse in warehouses
        }

        return products_per_warehouse
