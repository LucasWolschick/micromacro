from typing import Any, Awaitable, Callable
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

    async def consume(
        self,
        callback: Callable[[Rx, Callable[..., Awaitable[None]]], Any],
        no_ack: bool = True,
    ):
        async def inner(msg: aio_pika.abc.AbstractIncomingMessage):
            async def ack():
                if no_ack == False:
                    await msg.ack()

            rx = self.rx_cls.model_validate_json(msg.body.decode("utf-8"))
            await callback(rx, ack)

        await self.queue.consume(inner, no_ack=no_ack)


class QueueFactory:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    async def connect(self):
        self.connection = await aio_pika.connect(self.connection_string)
        self.channel = self.connection.channel()
        await self.channel.initialize()
        pass

    async def disconnect(self):
        await self.connection.close()

    async def make_send_queue[Tx: BaseModel](self, queue_name: str):
        queue: aio_pika.Queue = await self.channel.declare_queue(queue_name)  # type: ignore
        return SendQueue[Tx](queue)

    async def make_receive_queue[Rx: BaseModel](
        self, queue_name: str, message_cls: type[Rx]
    ):
        queue: aio_pika.Queue = await self.channel.declare_queue(queue_name)  # type: ignore
        return ReceiveQueue[Rx](queue, message_cls)
