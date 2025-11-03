from common.db.connection import ConnectionPool
from app.core.vendor import Vendor


class VendorRepository:
    def __init__(self, db: ConnectionPool):
        self.db = db

    async def insert(self, vendor: Vendor) -> Vendor:
        sql = """
            INSERT INTO vendors (username, password, ssn) VALUES ($1, $2, $3, $4) RETURNING (id, username, password, ssn);
        """

        async with self.db.get_conn() as conn:
            result = await conn.fetchrow(
                sql, vendor.username, vendor.password, vendor.ssn
            )

        assert result != None, "Could not insert vendor"

        return Vendor(result[0], result[1], result[2], result[3])

    async def get_by_id(self, id: int) -> Vendor:
        sql = """
            SELECT id, username, password, ssn FROM vendors WHERE id = $1;
        """

        async with self.db.get_conn() as conn:
            result = await conn.fetchrow(sql, id)

        assert result is not None, "Vendor not found"

        return Vendor(result[0], result[1], result[2], result[3])

    async def try_get_by_credentials(
        self, username: str, password: str
    ) -> Vendor | None:
        sql = """
            SELECT id, username, password, ssn FROM vendors WHERE username = $1 AND password = $2;
        """

        async with self.db.get_conn() as conn:
            result = await conn.fetchrow(sql, username, password)

        if result is None:
            return None

        return Vendor(result[0], result[1], result[2], result[3])
