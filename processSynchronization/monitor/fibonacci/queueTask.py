from typing import TYPE_CHECKING

from _logging import logger

if TYPE_CHECKING:
    from queue import Queue
    from threading import Condition


def queue_task(condition: "Condition", shared_q: "Queue", inputs: list[int]) -> None:
    logger.info("Starting queue task...")
    with condition:
        for _in in inputs:
            shared_q.put(_in)

        logger.debug(
            "Notifying fibonacci task threads that the queue is ready to consume..."
        )
        condition.notify_all()  # waiting queue에 있는 모든 thread를 깨운다.
