from httpx import AsyncClient

_http_client: AsyncClient | None = None


def set_http_client(db: AsyncClient):
    global _http_client
    _http_client = db


def get_http_client() -> AsyncClient:
    assert _http_client is not None, "HTTP client instance not set"
    return _http_client
