from pydantic import BaseModel
from common.queues.queue_factory import QueueFactory, SendQueue

type ProductCreatedQueue = SendQueue[ProductCreatedMessage]


class ProductCreatedMessage(BaseModel):
    product_id: int
    vendor_id: int


async def product_created_queue(
    queue_factory: QueueFactory,
) -> ProductCreatedQueue:
    return await queue_factory.make_send_queue("product_created")
