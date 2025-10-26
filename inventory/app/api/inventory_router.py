from typing import Annotated
from fastapi import APIRouter, Depends, Query

from common.db.deps import get_db
from common.db.connection import ConnectionPool

from app.repositories.stock_repository import StockRepository
from app.repositories.warehouse_repository import WarehouseRepository

from app.use_cases.list_stocks import ListStocksRequest, ListStocks
from app.use_cases.list_warehouses import ListWarehouses
from app.use_cases.set_stock import SetStock, SetStockRequest

router = APIRouter(prefix="/stocks")


@router.get("/warehouses")
async def list_warehouses(db: Annotated[ConnectionPool, Depends(get_db)]):
    warehouse_repo = WarehouseRepository(db)
    use_case = ListWarehouses(warehouse_repo)
    return await use_case.run()


@router.get("/")
async def list_stocks(
    db: Annotated[ConnectionPool, Depends(get_db)],
    products: Annotated[list[int] | None, Query()] = None,
    warehouse_id: Annotated[int | None, Query()] = None,
):
    request = ListStocksRequest(products=products, warehouse_id=warehouse_id)
    stocks_repo = StockRepository(db)
    warehouse_repo = WarehouseRepository(db)
    use_case = ListStocks(stocks_repo, warehouse_repo)
    return await use_case.run(request)


@router.post("/{id}")
async def set_stock(
    request: SetStockRequest, db: Annotated[ConnectionPool, Depends(get_db)]
):
    stocks_repo = StockRepository(db)
    warehouse_repo = WarehouseRepository(db)
    use_case = SetStock(stocks_repo, warehouse_repo)
    return await use_case.run(request)
