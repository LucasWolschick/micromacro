import logging
from typing import Awaitable, Callable
from fastapi import FastAPI, Request, Response
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse

from app.db.connection import ConnectionPool
from app.db.deps import set_db_instance
from app.exceptions import ApplicationException, NotFoundException
from app.api import product_router
from app.settings import settings

db = ConnectionPool(settings.connection_string, settings.db_name)
set_db_instance(db)

logging.basicConfig(level=settings.log)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
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
    except ApplicationException as e:
        return JSONResponse(status_code=400, content={"message": str(e)})


app.include_router(product_router.router)
