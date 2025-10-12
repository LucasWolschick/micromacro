from decimal import Decimal
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from app.repositories.product_repository import ProductRepository


class ListedProductModel(BaseModel):
    id: int
    description: str
    price: Decimal
    stock: Decimal


class ListProducts:
    def __init__(self, product_repository: Annotated[ProductRepository, Depends()]):
        self.product_repository = product_repository

    async def run(self) -> list[ListedProductModel]:
        products = await self.product_repository.list()
        return [
            ListedProductModel(
                id=p.id, description=p.description, price=p.price, stock=p.stock
            )
            for p in products
        ]
