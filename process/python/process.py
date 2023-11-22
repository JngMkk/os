import os

from multiprocessing import Process


def foo():
    print("Child PID:", os.getpid())
    print("My Parent PID:", os.getppid())


if __name__ == "__main__":
    print("Parent PID:", os.getpid())

    child = Process(target=foo).start()

"""
Parent PID: 5630
Child PID: 5657
My Parent PID: 5630
"""
