from .connection import ConnectionPool

_db_instance: ConnectionPool | None = None


def set_db_instance(db: ConnectionPool):
    global _db_instance
    _db_instance = db


def get_db() -> ConnectionPool:
    assert _db_instance is not None, "Database instance not set"
    return _db_instance
