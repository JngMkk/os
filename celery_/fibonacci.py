import logging

from app import app
from celery.result import AsyncResult
from tasks import fibo_task


def manage_fibo_task(values: list[int]) -> None:
    async_result_dict: dict[int, AsyncResult] = {
        value: fibo_task.apply_async(
            args=(value,), queue="fibo_queue", routing_key="fibo"
        )
        for value in values
    }

    for k, v in async_result_dict.items():
        # 아직 task를 처리하지 못했을 경우 AsyncResult.get() 메서드가 처리 결과를 얻지 못할 수 있음.
        # So, 결과를 얻을 준비가 됐는지 확인하는 AsyncResult.ready() 메서드를 결합.
        if v.ready():
            res = v.get(timeout=10)  # socket timeout
            logging.info(f"Value {k} -> {res}.")
        else:
            logging.info(f"Task {v.task_id} is not ready.")


if __name__ == "__main__":
    values = [4, 3, 8, 6, 10]
    manage_fibo_task(values)
