from .queue_factory import QueueFactory

_queue_factory: QueueFactory | None = None


def set_queue_factory(queue_factory: QueueFactory):
    global _queue_factory
    _queue_factory = queue_factory


def get_queue_factory() -> QueueFactory:
    assert _queue_factory is not None, "Queues factory instance not set"
    return _queue_factory
