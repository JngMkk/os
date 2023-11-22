import os

from multiprocessing import Process


def foo():
    print("Hello, OS!")
    print("My PID:", os.getpid())


if __name__ == "__main__":
    child1 = Process(target=foo).start()
    child2 = Process(target=foo).start()
    child3 = Process(target=foo).start()

"""
Hello, OS!
My PID: 5729
Hello, OS!
My PID: 5730
Hello, OS!
My PID: 5731
"""
