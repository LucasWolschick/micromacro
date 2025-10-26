from decimal import Decimal
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from app.repositories.product_repository import ProductRepository
from app.core.product import Product


class AddProductRequest(BaseModel):
    description: str
    price: Decimal


class AddProductResponse(BaseModel):
    id: int
    description: str
    price: Decimal


class AddProduct:
    def __init__(self, product_repository: Annotated[ProductRepository, Depends()]):
        self.product_repository = product_repository

    async def run(self, request: AddProductRequest) -> AddProductResponse:
        p = Product(
            id=0,
            description=request.description,
            price=request.price,
        )
        r = await self.product_repository.insert(p)
        return AddProductResponse(id=r.id, description=r.description, price=r.price)
