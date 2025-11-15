from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from app.queues.product_created import ProductCreatedMessage, ProductCreatedQueue
from app.repositories.product_repository import ProductRepository
from app.core.product import Product


class AddProductRequest(BaseModel):
    description: str
    price: float


class AddProductResponse(BaseModel):
    id: int
    description: str
    price: float
    vendor_id: int


class AddProduct:
    def __init__(
        self,
        product_repository: Annotated[ProductRepository, Depends()],
        product_created_queue: ProductCreatedQueue,
    ):
        self.product_repository = product_repository
        self.product_created_queue = product_created_queue

    async def run(
        self, request: AddProductRequest, vendor_id: int
    ) -> AddProductResponse:
        p = Product(
            id=0,
            description=request.description,
            price=request.price,
            vendor_id=vendor_id,
        )
        r = await self.product_repository.insert(p)
        await self.product_created_queue.send(
            ProductCreatedMessage(product_id=r.id, vendor_id=r.vendor_id)
        )
        return AddProductResponse(
            id=r.id, description=r.description, price=r.price, vendor_id=r.vendor_id
        )
