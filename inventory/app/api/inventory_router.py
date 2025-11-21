from typing import Annotated
from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from httpx import AsyncClient

from app.clients.client_factory import ClientFactory
from app.clients.deps import get_http_client
from app.clients.vendors_client import ValidateTokenResponse
from common.db.deps import get_db
from common.db.connection import ConnectionPool

from app.repositories.stock_repository import StockRepository
from app.repositories.warehouse_repository import WarehouseRepository

from app.use_cases.list_stocks import ListStocksRequest, ListStocks
from app.use_cases.list_warehouses import ListWarehouses
from app.use_cases.set_stock import SetStock, SetStockRequest
from app.use_cases.create_warehouse import CreateWarehouse, CreateWarehouseRequest

router = APIRouter(prefix="/stocks")
bearer = HTTPBearer()


async def auth(
    client: Annotated[AsyncClient, Depends(get_http_client)],
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
):
    vendors = ClientFactory(client).vendors()
    return await vendors.who_am_i(token.credentials)


@router.get("/warehouses")
async def list_warehouses(db: Annotated[ConnectionPool, Depends(get_db)]):
    warehouse_repo = WarehouseRepository(db)
    use_case = ListWarehouses(warehouse_repo)
    return await use_case.run()


@router.post("/warehouses")
async def create_warehouse(
    db: Annotated[ConnectionPool, Depends(get_db)],
    warehouse: CreateWarehouseRequest,
    _: Annotated[ValidateTokenResponse, Depends(auth)],
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
    _: Annotated[ValidateTokenResponse, Depends(auth)],
):
    stocks_repo = StockRepository(db)
    warehouse_repo = WarehouseRepository(db)
    use_case = SetStock(stocks_repo, warehouse_repo)
    return await use_case.run(
        SetStockRequest(product_id=product_id, warehouse_id=warehouse_id, stock=stock)
    )
