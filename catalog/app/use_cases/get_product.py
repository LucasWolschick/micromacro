from decimal import Decimal
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from app.repositories.product_repository import ProductRepository
from app.exceptions import ProductNotFoundException


class GetProductResponse(BaseModel):
    id: int
    description: str
    price: Decimal
    stock: Decimal


class GetProduct:
    def __init__(self, product_repository: Annotated[ProductRepository, Depends()]):
        self.product_repository = product_repository

    async def run(self, id: int) -> GetProductResponse:
        product = await self.product_repository.get(id)

        if product is None:
            raise ProductNotFoundException(id)

        return GetProductResponse(
            id=product.id,
            description=product.description,
            price=product.price,
            stock=product.stock,
        )
