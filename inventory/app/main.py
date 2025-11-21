import logging
from typing import Awaitable, Callable
from fastapi import FastAPI, Request, Response
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse

from common.db.connection import ConnectionPool
from common.db.deps import set_db_instance
from common.queues.queue_factory import QueueFactory
from common.queues.deps import set_queue_factory

from app.tasks.setup_tasks import setup_tasks
from app.exceptions import ApplicationException, NotFoundException
from app.api import health_router, inventory_router
from app.settings import settings

db = ConnectionPool(settings.connection_string, settings.db_name)
set_db_instance(db)

queue_factory = QueueFactory(settings.queues_connection_string)
set_queue_factory(queue_factory)

logging.basicConfig(level=settings.log)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    await queue_factory.connect()
    await setup_tasks()
    yield
    await queue_factory.disconnect()
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


app.include_router(health_router.router)
app.include_router(inventory_router.router)
