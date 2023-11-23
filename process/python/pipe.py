import os
import random
from multiprocessing import Pipe, Process
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from multiprocessing.connection import Connection


def producer_task(conn: "Connection") -> None:
    _randint = random.randint(1, 10)

    conn.send(_randint)
    print(f"Value {_randint} sent by PID {os.getpid()}. PPID: {os.getppid()}")
    conn.close()


def consumer_task(conn: "Connection") -> None:
    print(f"Value {conn.recv()} received by PID {os.getpid()}. PPID: {os.getppid()}")


if __name__ == "__main__":
    # 두 엔드포인트 (두 프로세스) 간의 통신을 구축하는 메커니즘으로 구성
    # 프로세스 간 메시지를 교환하기 위해 채널을 생성하는 방법
    producer_conn, consumer_conn = Pipe()  # 연결 객체 반환
    consumer = Process(target=consumer_task, args=(consumer_conn,))
    producer = Process(target=producer_task, args=(producer_conn,))

    # 실행 초기화
    consumer.start()
    producer.start()

    # 메인 프로세스가 자식 프로세스 실행을 기다림
    consumer.join()
    producer.join()


"""
Value 4 sent by PID 25253. PPID: 25225
Value 4 received by PID 25252. PPID: 25225
"""
