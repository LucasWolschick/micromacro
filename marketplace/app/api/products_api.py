from typing import Annotated
from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.security import OAuth2PasswordBearer
from httpx import AsyncClient

from app.clients.deps import get_http_client
from app.use_cases.add_product import AddProduct, AddProductRequest
from app.use_cases.get_product_availability import (
    GetProductAvailability,
    GetProductAvailabilityRequest,
)
from app.use_cases.list_products import ListProducts
from app.use_cases.get_product import GetProduct
from app.clients.client_factory import ClientFactory
from app.use_cases.update_stock import UpdateStock, UpdateStockRequest


router = APIRouter()
bearer = OAuth2PasswordBearer("/login")


@router.get("/products")
async def list_products(
    api_client: Annotated[AsyncClient, Depends(get_http_client)],
):
    factory = ClientFactory(api_client)
    use_case = ListProducts(factory.catalog(), factory.inventory())
    return await use_case.run()


@router.get("/products/{id}/stock")
async def get_product_availability(
    api_client: Annotated[AsyncClient, Depends(get_http_client)],
    product_id: Annotated[int, Path(alias="id")],
    quantity: Annotated[float, Query()] = 0.0,
):
    factory = ClientFactory(api_client)
    use_case = GetProductAvailability(factory.inventory())
    return await use_case.run(
        GetProductAvailabilityRequest(
            product_id=product_id, quantity_requested=quantity
        )
    )


@router.put("/products/{id}/stock")
async def update_stock(
    api_client: Annotated[AsyncClient, Depends(get_http_client)],
    product_id: Annotated[int, Path(alias="id")],
    warehouse_id: Annotated[int, Body()],
    quantity: Annotated[float, Body()],
    token: Annotated[str, Depends(bearer)],
):
    factory = ClientFactory(api_client)
    use_case = UpdateStock(factory.catalog(), factory.inventory())
    return await use_case.run(
        UpdateStockRequest(
            product_id=product_id, warehouse_id=warehouse_id, quantity=quantity
        ),
        token,
    )


@router.get("/products/{id}")
async def get_product(
    api_client: Annotated[AsyncClient, Depends(get_http_client)],
    product_id: int,
):
    factory = ClientFactory(api_client)
    use_case = GetProduct(factory.catalog(), factory.inventory())
    return await use_case.run(product_id)


@router.post("/products")
async def add_product(
    api_client: Annotated[AsyncClient, Depends(get_http_client)],
    token: Annotated[str, Depends(bearer)],
    request: AddProductRequest,
):
    factory = ClientFactory(api_client)
    use_case = AddProduct(factory.catalog())
    return await use_case.run(token, request)
