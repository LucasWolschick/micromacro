from pydantic import BaseModel
from common.queues.queue_factory import ReceiveQueue, QueueFactory

type ProductCreatedQueue = ReceiveQueue[ProductCreatedMessage]


class ProductCreatedMessage(BaseModel):
    product_id: int
    vendor_id: int


async def product_created_queue(queue_factory: QueueFactory):
    return await queue_factory.make_receive_queue(
        "product_created", ProductCreatedMessage
    )
