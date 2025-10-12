from typing import Annotated
from fastapi import APIRouter, Depends

from app.db.deps import get_db
from app.repositories.product_repository import ProductRepository
from app.use_cases.add_product import AddProduct, AddProductRequest
from app.db.connection import ConnectionPool
from catalog.app.use_cases.get_product import GetProduct, GetProductResponse
from catalog.app.use_cases.list_products import ListProducts, ListedProductModel

router = APIRouter(prefix="/products")


@router.post("/")
async def add_product(
    product: AddProductRequest, db: Annotated[ConnectionPool, Depends(get_db)]
):
    repo = ProductRepository(db)
    use_case = AddProduct(repo)
    return await use_case.run(product)


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
