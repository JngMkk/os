import os
import threading


def foo():
    print("PID:", os.getpid())
    print("Thread ID:", threading.get_native_id())


if __name__ == "__main__":
    print("PID:", os.getpid())
    t1 = threading.Thread(target=foo).start()


"""
PID: 6692
PID: 6692
Thread ID: 924557
"""
