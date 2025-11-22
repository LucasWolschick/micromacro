from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from httpx import AsyncClient

from app.clients.client_factory import ClientFactory
from app.clients.deps import get_http_client
from app.use_cases.add_warehouse import AddWarehouse, AddWarehouseRequest
from app.use_cases.list_warehouses import ListWarehouses


router = APIRouter(prefix="/inventory")
bearer = OAuth2PasswordBearer("/login")


@router.get("/warehouses")
async def get_warehouses(http_client: Annotated[AsyncClient, Depends(get_http_client)]):
    client_factory = ClientFactory(http_client)
    use_case = ListWarehouses(client_factory.inventory())
    return await use_case.run()


@router.post("/warehouses")
async def add_warehouse(
    http_client: Annotated[AsyncClient, Depends(get_http_client)],
    request: AddWarehouseRequest,
    token: Annotated[str, Depends(bearer)],
):
    client_factory = ClientFactory(http_client)
    use_case = AddWarehouse(client_factory.inventory())
    return await use_case.run(token, request)
