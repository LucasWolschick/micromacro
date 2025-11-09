from typing import Annotated

from fastapi import Depends

from common.db.connection import ConnectionPool
from common.db.deps import get_db

from app.core.product import Product


class ProductRepository:
    def __init__(self, db: Annotated[ConnectionPool, Depends(get_db)]):
        self.db = db

    async def get(self, id: int) -> Product | None:
        sql = """SELECT id, description, price FROM products WHERE id = $1;"""

        async with self.db.get_conn() as conn:
            result = await conn.fetch(sql, id)

        if len(result) == 0:
            return None

        r, *_ = result

        return Product(r["id"], r["description"], r["price"])

    async def insert(self, product: Product) -> Product:
        sql = """INSERT INTO products (description, price) VALUES ($1, $2) RETURNING id, description, price;"""

        async with self.db.get_conn() as conn:
            result = await conn.fetchrow(sql, product.description, product.price)

        assert result, "Failed to insert product"

        return Product(result["id"], result["description"], result["price"])

    async def list(self) -> list[Product]:
        sql = """SELECT id, description, price FROM products;"""

        async with self.db.get_conn() as conn:
            result = await conn.fetch(sql)

        return [Product(r["id"], r["description"], r["price"]) for r in result]
