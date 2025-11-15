from typing import Any, Awaitable, Callable, Coroutine
from app.queues.product_created import ProductCreatedMessage, ProductCreatedQueue
from app.repositories.stock_repository import StockRepository
from app.repositories.warehouse_repository import WarehouseRepository

from app.use_cases.list_warehouses import ListWarehouses
from app.use_cases.on_product_created import OnProductCreated
from app.use_cases.set_stock import SetStock
from common.db.connection import ConnectionPool


async def setup_on_product_created_task(db: ConnectionPool, queue: ProductCreatedQueue):
    async def handle_message(
        msg: ProductCreatedMessage, ack: Callable[..., Awaitable[None]]
    ):
        stock_repository = StockRepository(db)
        warehouse_repository = WarehouseRepository(db)
        set_stock = SetStock(stock_repository, warehouse_repository)
        list_warehouses = ListWarehouses(warehouse_repository)
        use_case = OnProductCreated(set_stock, list_warehouses)
        await use_case.run(msg)
        await ack()

    await queue.consume(handle_message)
