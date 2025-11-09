import logging
from typing import Awaitable, Callable
from fastapi import FastAPI, Request, Response
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
from httpx import AsyncClient

from common.db.connection import ConnectionPool
from common.db.deps import set_db_instance

from app.clients.deps import set_http_client, get_http_client
from app.exceptions import (
    ApplicationException,
    NotAuthenticatedException,
    NotFoundException,
)
from app.api import product_router
from app.settings import settings

db = ConnectionPool(settings.connection_string, settings.db_name)
set_db_instance(db)

logging.basicConfig(level=settings.log)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    set_http_client(AsyncClient())
    yield
    await get_http_client().aclose()
    await db.disconnect()


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def handle_exceptions(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    try:
        return await call_next(request)
    except NotFoundException as e:
        return JSONResponse(status_code=404, content={"message": str(e)})
    except NotAuthenticatedException as e:
        return JSONResponse(status_code=403, content={"message": str(e)})
    except ApplicationException as e:
        return JSONResponse(status_code=400, content={"message": str(e)})


app.include_router(product_router.router)
