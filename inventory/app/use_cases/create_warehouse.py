from pydantic import BaseModel

from app.repositories.warehouse_repository import WarehouseRepository
from app.core.warehouse import Warehouse


class CreateWarehouseRequest(BaseModel):
    description: str


class CreateWarehouseResponse(BaseModel):
    id: int
    description: str


class CreateWarehouse:
    def __init__(
        self,
        warehouse_repository: WarehouseRepository,
    ):
        self.warehouse_repository = warehouse_repository

    async def run(self, request: CreateWarehouseRequest) -> CreateWarehouseResponse:
        warehouse = await self.warehouse_repository.insert(
            Warehouse(0, request.description)
        )
        return CreateWarehouseResponse(
            id=warehouse.id, description=warehouse.description
        )
