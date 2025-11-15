from dataclasses import dataclass


@dataclass
class Stock:
    id: int
    product_id: int
    warehouse_id: int
    stock: float
