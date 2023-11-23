from threading import current_thread
from typing import TYPE_CHECKING

from _logging import logger

if TYPE_CHECKING:
    from queue import Queue
    from threading import Condition


fibo_dic = {}


def fibonacci(x: int) -> int:
    a, b = 0, 1
    for _ in range(x):
        a, b = b, a + b
        fibo_dic[x] = a


def fibonacci_task(condition: "Condition", shared_q: "Queue") -> None:
    # with문이 없다면 락 취득과 해제를 명시적으로 해야함.
    # with문과 함께 쓰면 내부 블록의 시작에서 락을 취득하고, 끝에 락을 해제할 수 있음.
    with condition:
        while shared_q.empty():
            logger.info(f"[{current_thread().name}] - waiting for elements in queue...")
            condition.wait()

        else:
            x = shared_q.get()
            fibonacci(x)

        shared_q.task_done()
        logger.debug(f"[{current_thread().name}] - Result [{fibo_dic[x]}]")
