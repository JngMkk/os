import threading


def foo():
    print("This is Foo.")
    print("Foo Thread ID:", threading.get_native_id())


def bar():
    print("This is Bar.")
    print("Bar Thread ID:", threading.get_native_id())


def baz():
    print("This is Baz.")
    print("Baz Thread ID:", threading.get_native_id())


if __name__ == "__main__":
    t1 = threading.Thread(target=foo).start()
    t2 = threading.Thread(target=bar).start()
    t3 = threading.Thread(target=baz).start()


"""
This is Foo.
Foo Thread ID: 927339
This is Bar.
Bar Thread ID: 927340
This is Baz.
Baz Thread ID: 927341
"""
