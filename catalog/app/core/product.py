from dataclasses import dataclass


@dataclass
class Product:
    id: int
    description: str
    price: float
    vendor_id: int
