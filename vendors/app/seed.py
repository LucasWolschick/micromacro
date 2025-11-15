import anyio
from common.db.deps import get_db
from app.repositories.vendor_repository import VendorRepository
from app.use_cases.register_vendor import RegisterVendor, RegisterVendorRequest
from app.settings import ENV


async def init_admin():
    if ENV is not "dev":
        return

    vendor_repo = VendorRepository(get_db())

    if await vendor_repo.try_get_by_username("admin") is not None:
        return

    use_case = RegisterVendor(vendor_repo)

    await use_case.run(
        RegisterVendorRequest(username="admin", password="admin", ssn="")
    )


async def seed():
    async with anyio.create_task_group() as tg:
        tg.start_soon(init_admin)
