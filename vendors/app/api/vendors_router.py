from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import SecretStr

from common.db.connection import ConnectionPool
from common.db.deps import get_db

from app.use_cases.register_vendor import RegisterVendor, RegisterVendorRequest
from app.repositories.vendor_repository import VendorRepository
from app.use_cases.auth_vendor import AuthVendor, AuthVendorRequest
from app.use_cases.validate_token import (
    ValidateToken,
    ValidateTokenRequest,
    ValidateTokenResponse,
)


router = APIRouter(prefix="/vendors")
scheme = OAuth2PasswordBearer(tokenUrl="/vendors/token")


async def authenticate(
    db: Annotated[ConnectionPool, Depends(get_db)],
    token: Annotated[str, Depends(scheme)],
):
    vendor_repository = VendorRepository(db)
    use_case = ValidateToken(vendor_repository)
    return await use_case.run(ValidateTokenRequest(token=SecretStr(token)))


@router.get("/token")
async def who_am_i(
    token: Annotated[ValidateTokenResponse, Depends(authenticate)],
):
    return token


@router.post("/")
async def register_vendor(
    db: Annotated[ConnectionPool, Depends(get_db)],
    vendor: RegisterVendorRequest,
    _: Annotated[ValidateTokenResponse, Depends(authenticate)],
):
    vendor_repository = VendorRepository(db)
    use_case = RegisterVendor(vendor_repository)
    return await use_case.run(vendor)


@router.post("/token")
async def auth_vendor(
    db: Annotated[ConnectionPool, Depends(get_db)],
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    vendor_repository = VendorRepository(db)
    use_case = AuthVendor(vendor_repository)
    return await use_case.run(
        AuthVendorRequest(username=credentials.username, password=credentials.password)
    )
