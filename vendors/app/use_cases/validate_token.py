from pydantic import BaseModel, SecretStr
from app.repositories.vendor_repository import VendorRepository
from app.crypto import jwt


class ValidateTokenRequest(BaseModel):
    token: SecretStr


class ValidateTokenResponse(BaseModel):
    id: int
    username: str


class ValidateToken:
    def __init__(self, vendor_repository: VendorRepository):
        self.vendor_repository = vendor_repository

    async def run(self, request: ValidateTokenRequest) -> ValidateTokenResponse:
        vendor_id = jwt.decode_vendor_id(request.token.get_secret_value())

        vendor = await self.vendor_repository.get_by_id(vendor_id)

        return ValidateTokenResponse(id=vendor.id, username=vendor.username)
