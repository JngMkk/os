import os

from multiprocessing import Process


def foo():
    print("This is Foo.")
    print("PID:", os.getpid())


def bar():
    print("This is Bar.")
    print("PID:", os.getpid())


def baz():
    print("This is Baz.")
    print("PID:", os.getpid())


if __name__ == "__main__":
    child1 = Process(target=foo).start()
    child2 = Process(target=bar).start()
    child3 = Process(target=baz).start()

"""
This is Foo.
PID: 5845
This is Bar.
PID: 5846
This is Baz.
PID: 5847
"""
