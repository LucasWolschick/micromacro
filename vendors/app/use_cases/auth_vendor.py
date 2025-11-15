from datetime import timedelta
from pydantic import BaseModel
from app.repositories.vendor_repository import VendorRepository
from app.exceptions import NotAuthenticatedException
from app.crypto import jwt, passwords


class AuthVendorRequest(BaseModel):
    username: str
    password: str


class AuthVendorResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthVendor:
    def __init__(self, vendor_repository: VendorRepository):
        self.vendor_repository = vendor_repository

    async def run(self, credentials: AuthVendorRequest) -> AuthVendorResponse:
        vendor = await self.vendor_repository.try_get_by_username(credentials.username)

        if vendor is None:
            raise NotAuthenticatedException()

        if not passwords.verify(credentials.password, vendor.password):
            raise NotAuthenticatedException()

        token = jwt.issue(vendor.id, timedelta(weeks=1))

        return AuthVendorResponse(access_token=token)
