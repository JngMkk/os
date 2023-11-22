import os
import threading


def foo():
    print("PID:", os.getpid())
    print("Thread ID:", threading.get_native_id())


if __name__ == "__main__":
    t1 = threading.Thread(target=foo).start()
    t2 = threading.Thread(target=foo).start()
    t3 = threading.Thread(target=foo).start()


"""
PID: 6905
Thread ID: 926514
PID: 6905
Thread ID: 926515
PID: 6905
Thread ID: 926516
"""
