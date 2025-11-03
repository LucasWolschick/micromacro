from dataclasses import dataclass


@dataclass
class Vendor:
    id: int
    username: str
    password: str
    ssn: str
