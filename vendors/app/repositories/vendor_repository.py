from common.db.connection import ConnectionPool
from app.core.vendor import Vendor


class VendorRepository:
    def __init__(self, db: ConnectionPool):
        self.db = db

    async def insert(self, vendor: Vendor) -> Vendor:
        sql = """
            INSERT INTO vendors (username, password, ssn) VALUES ($1, $2, $3) RETURNING *;
        """

        async with self.db.get_conn() as conn:
            result = await conn.fetchrow(
                sql, vendor.username, vendor.password, vendor.ssn
            )

        assert result != None, "Could not insert vendor"

        return Vendor(
            result["id"], result["username"], result["password"], result["ssn"]
        )

    async def get_by_id(self, id: int) -> Vendor:
        sql = """
            SELECT id, username, password, ssn FROM vendors WHERE id = $1;
        """

        async with self.db.get_conn() as conn:
            result = await conn.fetchrow(sql, id)

        assert result is not None, "Vendor not found"

        return Vendor(
            result["id"], result["username"], result["password"], result["ssn"]
        )

    async def try_get_by_username(self, username: str) -> Vendor | None:
        sql = """
            SELECT id, username, password, ssn FROM vendors WHERE username = $1;
        """

        async with self.db.get_conn() as conn:
            result = await conn.fetchrow(sql, username)

        if result is None:
            return None

        return Vendor(
            result["id"], result["username"], result["password"], result["ssn"]
        )
