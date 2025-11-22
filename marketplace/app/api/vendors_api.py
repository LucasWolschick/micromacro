from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from httpx import AsyncClient
from pydantic import SecretStr

from app.clients.client_factory import ClientFactory
from app.clients.deps import get_http_client
from app.use_cases.login import Login, LoginRequest

router = APIRouter()


@router.post("/login")
async def login(
    http_client: Annotated[AsyncClient, Depends(get_http_client)],
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    client_factory = ClientFactory(http_client)
    use_case = Login(client_factory.vendors())
    token = await use_case.run(
        LoginRequest(
            user=credentials.username, password=SecretStr(credentials.password)
        )
    )
    return {"access_token": token.token, "token_type": "bearer"}
