from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Stock:
    id: int
    product_id: int
    warehouse_id: int
    stock: Decimal
