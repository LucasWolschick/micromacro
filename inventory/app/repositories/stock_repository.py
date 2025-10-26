from typing import Annotated

from fastapi import Depends

from common.db.connection import ConnectionPool
from common.db.deps import get_db

from app.core.stock import Stock


class StockRepository:
    def __init__(self, db: Annotated[ConnectionPool, Depends(get_db)]):
        self.db = db

    async def get(self, id: int) -> Stock | None:
        sql = (
            """SELECT id, product_id, warehouse_id, stock FROM stocks WHERE id = $1;"""
        )

        async with self.db.get_conn() as conn:
            result = await conn.fetch(sql, id)

        if len(result) == 0:
            return None

        r, *_ = result

        return Stock(r["id"], r["product_id"], r["warehouse_id"], r["stock"])

    async def set(self, stock: Stock) -> Stock:
        sql = """INSERT INTO stocks
                    (product_id, warehouse_id, stock)
                VALUES
                    ($1, $2, $3)
                ON CONFLICT (product_id, warehouse_id) DO UPDATE SET
                    stock = $3
                RETURNING *;"""

        async with self.db.get_conn() as conn:
            result = await conn.fetchrow(sql, stock.product_id, stock.stock)

        assert result, "Failed to set stock"

        return Stock(
            result["id"], result["product_id"], result["warehouse_id"], result["stock"]
        )

    async def list_from_warehouse(self, warehouse_id: int) -> list[Stock]:
        sql = """SELECT id, product_id, warehouse_id, stock FROM stocks WHERE warehouse_id = $1;"""

        async with self.db.get_conn() as conn:
            result = await conn.fetch(sql, warehouse_id)

        return [
            Stock(r["id"], r["product_id"], r["warehouse_id"], r["stock"])
            for r in result
        ]

    async def list(self) -> list[Stock]:
        sql = """SELECT id, product_id, warehouse_id, stock FROM stocks;"""

        async with self.db.get_conn() as conn:
            result = await conn.fetch(sql)

        return [
            Stock(r["id"], r["product_id"], r["warehouse_id"], r["stock"])
            for r in result
        ]
