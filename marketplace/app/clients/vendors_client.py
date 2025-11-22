from http import HTTPStatus
from typing import Literal
import urllib.parse
from httpx import AsyncClient
from pydantic import BaseModel

from app.exceptions import NotAuthenticatedException


class ValidateTokenResponse(BaseModel):
    id: int
    username: str


class GetTokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]


class VendorsClient:
    def __init__(self, base_url: str, client: AsyncClient):
        self.base_url = base_url
        self.client = client

    async def get_token(self, user: str, password: str):
        url = urllib.parse.urljoin(self.base_url, "/vendors/token")

        response = await self.client.post(
            url, data={"grant_type": "password", "username": user, "password": password}
        )

        if response.status_code == HTTPStatus.FORBIDDEN:
            raise NotAuthenticatedException()

        response.raise_for_status()

        return GetTokenResponse(**response.json())

    async def who_am_i(self, token: str):
        url = urllib.parse.urljoin(self.base_url, "/vendors/token")

        response = await self.client.get(
            url, headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code == HTTPStatus.FORBIDDEN:
            raise NotAuthenticatedException()

        response.raise_for_status()

        return ValidateTokenResponse(**response.json())
