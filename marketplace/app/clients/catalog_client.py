from decimal import Decimal
from http import HTTPStatus
from httpx import AsyncClient
from pydantic import BaseModel
import urllib.parse

from app.exceptions import ProductNotFoundException


class AddProductRequest(BaseModel):
    description: str
    price: Decimal


class AddProductResponse(BaseModel):
    id: int
    description: str
    price: Decimal


class GetProductResponse(BaseModel):
    id: int
    description: str
    price: Decimal


class ListedProductModel(BaseModel):
    id: int
    description: str
    price: Decimal


class CatalogClient:
    def __init__(self, base_url: str, client: AsyncClient):
        self.base_url = base_url
        self.client = client

    async def add_product(self, product: AddProductRequest) -> AddProductResponse:
        url = urllib.parse.urljoin(self.base_url, "/products")

        response = await self.client.post(url, json=product.model_dump())
        response.raise_for_status()

        return AddProductResponse(**response.json())

    async def get_product(self, id: int) -> GetProductResponse:
        url = urllib.parse.urljoin(self.base_url, f"/products/product/{id}")

        response = await self.client.get(url)

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise ProductNotFoundException(id)

        response.raise_for_status()

        return GetProductResponse(**response.json())

    async def list_products(self) -> list[ListedProductModel]:
        url = urllib.parse.urljoin(self.base_url, "/products/product")

        response = await self.client.get(url)
        response.raise_for_status()

        return [ListedProductModel(**product) for product in response.json()]
