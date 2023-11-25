import sys

from cutlery import Cutlery
from threadbot import ThreadBot

if __name__ == "__main__":
    kitchen = Cutlery(knives=100, forks=100)
    bots = [ThreadBot(kitchen) for _ in range(10)]

    for bot in bots:
        for _ in range(int(sys.argv[1])):
            bot.tasks.put("prepare-table")
            bot.tasks.put("clear-table")

        bot.tasks.put("shutdown")

    print("Kitchen inventory before service:", kitchen)
    for bot in bots:
        bot.start()

    for bot in bots:
        bot.join()

    print("Kitchen inventory after service:", kitchen)


"""
Kitchen inventory before service: Cutlery(knives=100, forks=100, lock=<unlocked _thread.lock object at 0x10319a680>)
Kitchen inventory after service: Cutlery(knives=100, forks=100, lock=<unlocked _thread.lock object at 0x10319a680>)
"""
