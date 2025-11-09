from typing import Annotated

from fastapi import Depends

from common.db.connection import ConnectionPool
from common.db.deps import get_db

from app.core.warehouse import Warehouse


class WarehouseRepository:
    def __init__(self, db: Annotated[ConnectionPool, Depends(get_db)]):
        self.db = db

    async def exists(self, id: int) -> bool:
        sql = """SELECT 1 FROM warehouses WHERE id = $1;"""

        async with self.db.get_conn() as conn:
            result = await conn.fetchval(sql, id)

        return result is not None

    async def insert(self, warehouse: Warehouse) -> Warehouse:
        sql = """INSERT INTO warehouses (description) VALUES ($1) RETURNING id, description;"""

        async with self.db.get_conn() as conn:
            result = await conn.fetchrow(sql, warehouse.description)

        assert result is not None, "Error inserting warehouse"

        return Warehouse(result["id"], result["description"])

    async def list(self) -> list[Warehouse]:
        sql = """SELECT id, description FROM warehouses;"""

        async with self.db.get_conn() as conn:
            result = await conn.fetch(sql)

        return [Warehouse(r["id"], r["description"]) for r in result]
