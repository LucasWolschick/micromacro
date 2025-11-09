from typing import Annotated

from fastapi import Depends

from common.db.connection import ConnectionPool
from common.db.deps import get_db

from app.core.product import Product


class ProductRepository:
    def __init__(self, db: Annotated[ConnectionPool, Depends(get_db)]):
        self.db = db

    async def get(self, id: int) -> Product | None:
        sql = (
            """SELECT id, description, price, vendor_id FROM products WHERE id = $1;"""
        )

        async with self.db.get_conn() as conn:
            result = await conn.fetch(sql, id)

        if len(result) == 0:
            return None

        r, *_ = result

        return Product(r["id"], r["description"], r["price"], r["vendor_id"])

    async def insert(self, product: Product) -> Product:
        sql = """INSERT INTO products (description, price, vendor_id) VALUES ($1, $2, $3) RETURNING id, description, price, vendor_id;"""

        async with self.db.get_conn() as conn:
            result = await conn.fetchrow(
                sql, product.description, product.price, product.vendor_id
            )

        assert result, "Failed to insert product"

        return Product(
            result["id"], result["description"], result["price"], result["vendor_id"]
        )

    async def list(self) -> list[Product]:
        sql = """SELECT id, description, price, vendor_id FROM products;"""

        async with self.db.get_conn() as conn:
            result = await conn.fetch(sql)

        return [
            Product(r["id"], r["description"], r["price"], r["vendor_id"])
            for r in result
        ]
