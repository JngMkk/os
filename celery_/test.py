import logging

from app import app
from celery.result import AsyncResult


def manage_sqrt_task(num: int) -> None:
    result: AsyncResult = app.send_task(
        "tasks.sqrt_task", args=(num,), queue="sqrt_queue", routing_key="sqrt"
    )
    logging.info(result.get())


if __name__ == "__main__":
    manage_sqrt_task(4)
