from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from httpx import AsyncClient

from app.queues.product_created import product_created_queue
from common.db.deps import get_db
from common.db.connection import ConnectionPool
from common.queues.deps import get_queue_factory
from common.queues.queue_factory import QueueFactory

from app.repositories.product_repository import ProductRepository
from app.use_cases.add_product import AddProduct, AddProductRequest
from app.use_cases.get_product import GetProduct, GetProductResponse
from app.use_cases.list_products import ListProducts, ListedProductModel
from app.clients.deps import get_http_client
from app.clients.vendors_client import ValidateTokenResponse
from app.clients.client_factory import ClientFactory

router = APIRouter(prefix="/products")
bearer = HTTPBearer()


async def auth(
    client: Annotated[AsyncClient, Depends(get_http_client)],
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
):
    vendors = ClientFactory(client).vendors()
    return await vendors.who_am_i(token.credentials)


@router.post("/")
async def add_product(
    vendor: Annotated[ValidateTokenResponse, Depends(auth)],
    product: AddProductRequest,
    db: Annotated[ConnectionPool, Depends(get_db)],
    queue_factory: Annotated[QueueFactory, Depends(get_queue_factory)],
):
    repo = ProductRepository(db)
    queue = await product_created_queue(queue_factory)
    use_case = AddProduct(repo, queue)
    return await use_case.run(product, vendor.id)


@router.get("/product/{id}")
async def get_product(
    id: int, db: Annotated[ConnectionPool, Depends(get_db)]
) -> GetProductResponse:
    repo = ProductRepository(db)
    use_case = GetProduct(repo)
    return await use_case.run(id)


@router.get("/product")
async def list_products(
    db: Annotated[ConnectionPool, Depends(get_db)],
) -> list[ListedProductModel]:
    repo = ProductRepository(db)
    use_case = ListProducts(repo)
    return await use_case.run()
