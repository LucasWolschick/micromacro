from http import HTTPStatus
import urllib.parse
from httpx import AsyncClient
from pydantic import BaseModel

from app.exceptions import NotAuthenticatedException


class ValidateTokenResponse(BaseModel):
    id: int
    username: str


class VendorsClient:
    def __init__(self, base_url: str, client: AsyncClient):
        self.base_url = base_url
        self.client = client

    async def who_am_i(self, token: str):
        url = urllib.parse.urljoin(self.base_url, "/token")

        response = await self.client.get(
            url, headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise NotAuthenticatedException()

        response.raise_for_status()

        return ValidateTokenResponse(**response.json())
