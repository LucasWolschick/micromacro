from typing import Annotated
from fastapi import APIRouter, Depends
from httpx import AsyncClient

from app.clients.deps import get_http_client
from app.use_cases.list_products import ListProducts
from app.use_cases.get_product import GetProduct
from app.clients.client_factory import ClientFactory


router = APIRouter()


@router.get("/products")
async def list_products(api_client: Annotated[AsyncClient, Depends(get_http_client)]):
    factory = ClientFactory(api_client)
    use_case = ListProducts(factory.catalog(), factory.inventory())
    return await use_case.run()


@router.get("/products/{id}")
async def get_product(
    api_client: Annotated[AsyncClient, Depends(get_http_client)], product_id: int
):
    factory = ClientFactory(api_client)
    use_case = GetProduct(factory.catalog(), factory.inventory())
    return await use_case.run(product_id)
