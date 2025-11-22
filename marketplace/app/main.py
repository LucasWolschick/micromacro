import logging
from typing import Awaitable, Callable
from fastapi import FastAPI, Request, Response
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

from common.db.connection import ConnectionPool
from common.db.deps import set_db_instance

from app.exceptions import (
    ApplicationException,
    NotAuthenticatedException,
    NotFoundException,
)
from app.settings import settings
from app.api import health_router, inventory_api, products_api, vendors_api
from app.clients.deps import get_http_client, set_http_client

db = ConnectionPool(settings.connection_string, settings.db_name)
set_db_instance(db)

logging.basicConfig(level=settings.log)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    set_http_client(httpx.AsyncClient())
    yield
    await get_http_client().aclose()
    await db.disconnect()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:5173",
    "https://localhost:5173",
    "http://localhost:8080",
    "https://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def handle_exceptions(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    try:
        return await call_next(request)
    except NotFoundException as e:
        return JSONResponse(status_code=404, content={"message": str(e)})
    except NotAuthenticatedException as e:
        return JSONResponse(status_code=401, content={"message": str(e)})
    except ApplicationException as e:
        return JSONResponse(status_code=400, content={"message": str(e)})


app.include_router(health_router.router)
app.include_router(products_api.router)
app.include_router(inventory_api.router)
app.include_router(vendors_api.router)
