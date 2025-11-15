import aio_pika
from pydantic import BaseModel


class SendQueue[Tx: BaseModel]:
    def __init__(self, queue: aio_pika.Queue):
        self.queue = queue

    async def send(self, data: Tx):
        await self.queue.channel.default_exchange.publish(
            aio_pika.Message(data.model_dump_json().encode("utf-8")),
            self.queue.name,
        )


class ReceiveQueue[Rx: BaseModel]:
    def __init__(self, queue: aio_pika.Queue, rx_cls: type[Rx]):
        self.queue = queue
        self.rx_cls = rx_cls

    async def recv(self):
        async for message in self.queue:
            yield self.rx_cls.model_validate_json(message.body.decode("utf-8"))


class QueueFactory:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.connection_string)
        self.channel = self.connection.channel()

    async def disconnect(self):
        await self.channel.close()
        await self.connection.close()

    async def make_send_queue[Tx: BaseModel](self, queue_name: str):
        queue: aio_pika.Queue = await self.channel.declare_queue(queue_name)  # type: ignore
        return SendQueue[Tx](queue)

    async def make_receive_queue[Rx: BaseModel](
        self, queue_name: str, message_cls: type[Rx]
    ):
        queue: aio_pika.Queue = await self.channel.declare_queue(queue_name)  # type: ignore
        return ReceiveQueue[Rx](queue, message_cls)
