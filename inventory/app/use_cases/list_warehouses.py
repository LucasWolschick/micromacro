from pydantic import BaseModel

from app.repositories.warehouse_repository import WarehouseRepository


class ListedWarehouseModel(BaseModel):
    id: int
    description: str


class ListWarehouses:
    def __init__(
        self,
        warehouse_repository: WarehouseRepository,
    ):
        self.warehouse_repository = warehouse_repository

    async def run(self) -> list[ListedWarehouseModel]:
        return [
            ListedWarehouseModel(id=warehouse.id, description=warehouse.description)
            for warehouse in await self.warehouse_repository.list()
        ]
