from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Product:
    id: int
    description: str
    price: Decimal
    stock: Decimal
