from typing import Annotated
from fastapi import APIRouter, Body, Depends, Path, Query

from common.db.deps import get_db
from common.db.connection import ConnectionPool

from app.repositories.stock_repository import StockRepository
from app.repositories.warehouse_repository import WarehouseRepository

from app.use_cases.list_stocks import ListStocksRequest, ListStocks
from app.use_cases.list_warehouses import ListWarehouses
from app.use_cases.set_stock import SetStock, SetStockRequest
from app.use_cases.create_warehouse import CreateWarehouse, CreateWarehouseRequest

router = APIRouter(prefix="/stocks")


@router.get("/warehouses")
async def list_warehouses(db: Annotated[ConnectionPool, Depends(get_db)]):
    warehouse_repo = WarehouseRepository(db)
    use_case = ListWarehouses(warehouse_repo)
    return await use_case.run()


@router.post("/warehouses")
async def create_warehouse(
    db: Annotated[ConnectionPool, Depends(get_db)], warehouse: CreateWarehouseRequest
):
    warehouse_repo = WarehouseRepository(db)
    use_case = CreateWarehouse(warehouse_repo)
    return await use_case.run(warehouse)


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
    db: Annotated[ConnectionPool, Depends(get_db)],
    product_id: Annotated[int, Path(alias="id")],
    warehouse_id: Annotated[int, Body()],
    stock: Annotated[float, Body()],
):
    stocks_repo = StockRepository(db)
    warehouse_repo = WarehouseRepository(db)
    use_case = SetStock(stocks_repo, warehouse_repo)
    return await use_case.run(
        SetStockRequest(product_id=product_id, warehouse_id=warehouse_id, stock=stock)
    )
