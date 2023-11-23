import logging
import multiprocessing
import random

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(message)s")

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


def producer_task(q: multiprocessing.Queue, fibo_dic: dict[int, int]) -> None:
    for _ in range(10):
        _randint = random.randint(1, 20)
        fibo_dic[_randint] = None
        logger.info(
            f"Producer {multiprocessing.current_process().name} putting value {_randint} into queue..."
        )
        q.put(_randint)


def consumer_task(q: multiprocessing.Queue, fibo_dic: dict[int, int]) -> None:
    while not q.empty():
        val = q.get(True, 0.05)
        a, b = 0, 1
        for _ in range(val):
            a, b = b, a + b
            fibo_dic[val] = a

        logger.info(
            f"Consumer {multiprocessing.current_process().name} getting value {val} from queue..."
        )


if __name__ == "__main__":
    # queue.Queue()와 비슷
    # But, 내부 구현에서 feeder thread를 호출하는 다른 메커니즘을 사용
    # feeder thread는 queue의 데이터 버퍼부터 도착지 프로세스와 관련된 파이프까지 데이터를 전달
    # Pipe와 multiprocessing.Queue 메커니즘 둘 다 메시지 전달 패러다임을 사용
    # lock 동기화 메커니즘을 사용할 필요가 없을지라도 내부적으로는 통신을 구축하기 위해 버퍼와 파이프 사이에 데이터를 전송할 때 동기화 메커니즘을 사용
    queue = multiprocessing.Queue()
    num_of_cpus = multiprocessing.cpu_count()  # 머신에서 CPU 양을 취득할 수 있는 함수 (8 cores)
    manager = multiprocessing.Manager()  # 프록시의 도움으로 다른 프로세스 간 파이썬 객체를 공유할 수 있도록 함
    fibo_dic = manager.dict()

    producer = multiprocessing.Process(target=producer_task, args=(queue, fibo_dic))
    producer.start()
    producer.join()

    consumers: list[multiprocessing.Process] = []
    for _ in range(num_of_cpus):
        consumer = multiprocessing.Process(target=consumer_task, args=(queue, fibo_dic))
        consumer.start()
        consumers.append(consumer)

    for consumer in consumers:
        consumer.join()

    logger.info(fibo_dic)


"""
2023-11-23 17:55:42,363 - Producer Process-2 putting value 14 into queue...
2023-11-23 17:55:42,364 - Producer Process-2 putting value 14 into queue...
2023-11-23 17:55:42,364 - Producer Process-2 putting value 17 into queue...
2023-11-23 17:55:42,364 - Producer Process-2 putting value 1 into queue...
2023-11-23 17:55:42,364 - Producer Process-2 putting value 12 into queue...
2023-11-23 17:55:42,364 - Producer Process-2 putting value 11 into queue...
2023-11-23 17:55:42,364 - Producer Process-2 putting value 12 into queue...
2023-11-23 17:55:42,364 - Producer Process-2 putting value 15 into queue...
2023-11-23 17:55:42,364 - Producer Process-2 putting value 14 into queue...
2023-11-23 17:55:42,364 - Producer Process-2 putting value 12 into queue...
2023-11-23 17:55:42,417 - Consumer Process-3 getting value 1 from queue...
2023-11-23 17:55:42,418 - Consumer Process-9 getting value 14 from queue...
2023-11-23 17:55:42,418 - Consumer Process-4 getting value 14 from queue...
2023-11-23 17:55:42,419 - Consumer Process-3 getting value 12 from queue...
2023-11-23 17:55:42,420 - Consumer Process-7 getting value 17 from queue...
2023-11-23 17:55:42,420 - Consumer Process-6 getting value 11 from queue...
2023-11-23 17:55:42,420 - Consumer Process-4 getting value 14 from queue...
2023-11-23 17:55:42,420 - Consumer Process-5 getting value 12 from queue...
2023-11-23 17:55:42,421 - Consumer Process-9 getting value 15 from queue...
2023-11-23 17:55:42,421 - Consumer Process-3 getting value 12 from queue...
2023-11-23 17:55:42,433 - {14: 377, 17: 1597, 1: 1, 12: 144, 11: 89, 15: 610}
"""
