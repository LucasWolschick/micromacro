class ApplicationException(Exception):
    pass


class NotFoundException(ApplicationException):
    pass


class StockNotFoundException(NotFoundException):
    def __init__(self, product_id: int, warehouse_id: int):
        super().__init__(
            f"Stock for product id '{product_id}' at warehouse '{warehouse_id}' not found"
        )
        self.product_id = product_id
        self.warehouse_id = warehouse_id


class WarehouseNotFoundException(NotFoundException):
    def __init__(self, id: int):
        super().__init__(f"Warehouse '{id}' not found")
        self.id = id
