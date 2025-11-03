from pydantic import BaseModel
from app.core.vendor import Vendor
from app.repositories.vendor_repository import VendorRepository
from app.exceptions import VendorAlreadyRegisteredException
from app.crypto import passwords


class RegisterVendorRequest(BaseModel):
    username: str
    password: str
    ssn: str


class RegisterVendorResponse(BaseModel):
    username: str
    ssn: str


class RegisterVendor:
    def __init__(self, vendor_repository: VendorRepository):
        self.vendor_repository = vendor_repository

    async def run(self, vendor: RegisterVendorRequest) -> RegisterVendorResponse:
        try:
            result = await self.vendor_repository.insert(
                Vendor(0, vendor.username, passwords.hash(vendor.password), vendor.ssn)
            )
            return RegisterVendorResponse(username=result.username, ssn=result.ssn)
        except:
            raise VendorAlreadyRegisteredException()
