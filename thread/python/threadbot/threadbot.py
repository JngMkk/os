import threading
from queue import Queue

from cutlery import Cutlery


class ThreadBot(threading.Thread):
    def __init__(self, kitchen: Cutlery) -> None:
        super().__init__(target=self.manage_table)
        self.kitchen = kitchen
        self.cutlery = Cutlery(knives=0, forks=0)
        self.tasks = Queue()

    def manage_table(self) -> None:
        while True:
            task = self.tasks.get()
            if task == "prepare-table":
                self.kitchen.give(to=self.cutlery, knives=4, forks=4)
            elif task == "clear-table":
                self.cutlery.give(to=self.kitchen, knives=4, forks=4)
            elif task == "shutdown":
                return
