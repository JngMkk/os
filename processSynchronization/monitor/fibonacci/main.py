import threading
from queue import Queue

from _logging import logger
from fibo import fibo_dic, fibonacci_task
from queueTask import queue_task

shared_q = Queue()  # 스레드 간 공유된 데이터의 컨테이너
inputs = [3, 10, 5, 7]

# 조건 변수.
# 특정 조건에 따라 자원 접근 시 동기화하는 것이 목적.
# 큐 생성을 제어하고 큐에서 발생한 것을 처리함.
q_condition = threading.Condition()

threads = [
    threading.Thread(target=fibonacci_task, args=(q_condition, shared_q), daemon=True)
    for _ in range(4)
]

for thread in threads:
    thread.start()

prod = threading.Thread(
    target=queue_task,
    name="queue_task_thread",
    args=(q_condition, shared_q, inputs),
    daemon=True,
)
prod.start()

for thread in threads:
    # 처리를 완료하기 전에 프로그램의 주요 흐름이 끝나지 않도록 메인 스레드가 임계 구역을 실행하는 스레드를 기다리는 것.
    thread.join()

logger.info(f"[{threading.current_thread().name}] - Result {fibo_dic}")


"""
fibonacci task 스레드는 순차 로직을 따라 실행하지 않음.
실행할 때마다 순서가 달라질 수 있음. 이것은 스레드 사용에 따른 특성 중 하나인 비결정성.

2023-11-23 15:24:20,673 - [Thread-1 (fibonacci_task)] - waiting for elements in queue...
2023-11-23 15:24:20,673 - [Thread-2 (fibonacci_task)] - waiting for elements in queue...
2023-11-23 15:24:20,673 - [Thread-3 (fibonacci_task)] - waiting for elements in queue...
2023-11-23 15:24:20,673 - [Thread-4 (fibonacci_task)] - waiting for elements in queue...
2023-11-23 15:24:20,673 - Starting queue task...
2023-11-23 15:24:20,673 - Notifying fibonacci task threads that the queue is ready to consume...
2023-11-23 15:24:20,673 - [Thread-1 (fibonacci_task)] - Result [2]
2023-11-23 15:24:20,673 - [Thread-3 (fibonacci_task)] - Result [55]
2023-11-23 15:24:20,673 - [Thread-4 (fibonacci_task)] - Result [5]
2023-11-23 15:24:20,673 - [Thread-2 (fibonacci_task)] - Result [13]
2023-11-23 15:24:20,673 - [MainThread] - Result [{3: 2, 10: 55, 5: 5, 7: 13}]
"""
