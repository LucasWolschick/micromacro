from app.queues.product_created import ProductCreatedMessage

from app.use_cases.list_warehouses import ListWarehouses
from app.use_cases.set_stock import SetStock, SetStockRequest


class OnProductCreated:
    def __init__(self, set_stock: SetStock, list_warehouses: ListWarehouses):
        self.set_stock = set_stock
        self.list_warehouses = list_warehouses
        pass

    async def run(self, product_created_message: ProductCreatedMessage):
        warehouses = await self.list_warehouses.run()
        for warehouse in warehouses:
            await self.set_stock.run(
                SetStockRequest(
                    product_id=product_created_message.product_id,
                    warehouse_id=warehouse.id,
                    stock=0,
                )
            )
