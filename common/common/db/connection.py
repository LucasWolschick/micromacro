import asyncio
from pathlib import Path
import asyncpg
import logging

from fastapi.concurrency import asynccontextmanager

logger = logging.getLogger(__name__)


class ConnectionPool:
    pool: asyncpg.Pool | None

    def __init__(self, connection_string: str, db_name: str):
        self.pool = None
        self.connection_string = connection_string
        self.db_name = db_name

    async def connect(self):
        assert self.pool is None

        while True:
            try:
                await self._ensure_database()
                self.pool = await asyncpg.create_pool(
                    f"{self.connection_string}{self.db_name}"
                )
                logger.info(f"Connected successfully to {self.db_name}")
                await self._sync_migrations()
                return
            except ConnectionRefusedError:
                logger.warning("db not up yet...")
                await asyncio.sleep(3)

    async def disconnect(self):
        assert self.pool is not None
        await self.pool.close()

    @asynccontextmanager
    async def get_conn(self):
        assert self.pool
        conn = await self.pool.acquire()
        try:
            yield conn
        finally:
            await self.pool.release(conn)

    async def _ensure_database(self):
        try:
            conn = await asyncpg.connect(f"{self.connection_string}{self.db_name}")
            await conn.close()
        except asyncpg.InvalidCatalogNameError:
            conn = await asyncpg.connect(f"{self.connection_string}")
            await conn.execute(f'CREATE DATABASE "{self.db_name}"')
            await conn.close()

    async def _sync_migrations(self):
        assert self.pool

        logger.info("Syncing migrations...")

        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS migrations (
                    migration_name TEXT PRIMARY KEY NOT NULL
                );
                """
            )

            available = sorted(
                (Path(p) for p in Path("app/db/migrations").glob("*.sql")),
                key=lambda p: p.name,
            )
            applied: set[str] = set(
                r[0] for r in await conn.fetch("SELECT migration_name FROM migrations;")
            )

            for m in available:
                if m.name in applied:
                    continue

                logger.info(f"Applying migration {m.name}:")

                with open(m, encoding="utf-8") as file:
                    src = file.read()

                logger.info(f"[{m.relative_to("app")}]=\n{src}")

                async with conn.transaction():
                    await conn.execute(src)
                    await conn.execute(
                        "INSERT INTO migrations (migration_name) VALUES ($1);", m.name
                    )

        logger.info("Synced with migrations.")
