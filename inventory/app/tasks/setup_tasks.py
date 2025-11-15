from common.db.deps import get_db
from common.queues.deps import get_queue_factory

from app.queues.product_created import product_created_queue
from app.tasks.on_product_created_task import setup_on_product_created_task


async def setup_tasks():
    db = get_db()
    queue_factory = get_queue_factory()

    await setup_on_product_created_task(db, await product_created_queue(queue_factory))
