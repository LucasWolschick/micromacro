from pydantic import BaseModel, SecretStr
from app.clients.vendors_client import VendorsClient


class LoginRequest(BaseModel):
    user: str
    password: SecretStr


class LoginResponse(BaseModel):
    token: str


class Login:
    def __init__(self, vendors_client: VendorsClient):
        self.vendors_client = vendors_client

    async def run(self, request: LoginRequest):
        response = await self.vendors_client.get_token(
            request.user, request.password.get_secret_value()
        )
        return LoginResponse(token=response.access_token)
