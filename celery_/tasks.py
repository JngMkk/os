import time
from math import sqrt

from app import app


@app.task
def sqrt_task(num: int) -> float:
    return sqrt(num)


@app.task(bind=True)
def fibo_task(self, num: int) -> str:
    a, b = 0, 1
    for _ in range(num):
        a, b = b, a + b

    message = f"Fibonacci calculated with task id {self.request.id}. Result is {a}."
    return message
