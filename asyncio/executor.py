import asyncio
import time

"""
때로 별도의 스레드나 프로세스에서 작업을 수행해야 할 수 있음.
loop.run_in_executor(None, func)
이 문법으로 블로킹 함수를 전달하여 기본 익스큐터에서 실행되도록 요청함.
run_in_executor()는 메인 스레드 자체를 블로킹하지 않는다. 단지 익스큐터에 작업을 스케줄링하는 것뿐.
run_in_executor()를 호출하면 Future 객체를 반환받는데, 다른 코루틴 함수에서 호출했다면 await 키워드를 통해 블로킹 함수의 실행이 완료될 때까지 대기할 수도 있음.
"""


async def main():
    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(1.0)
    await loop.run_in_executor(None, blocking)
    print(f"{time.ctime()} GoodBye!")


def blocking():
    # time.sleep()을 호출함으로 인해 메인 스레드에서 해당 함수를 호출하면 메인 스레드를 블로킹하고 이벤트 루프를 실행되지 않도록 함
    # 즉, asyncio 루프가 실행되고 있는 메인 스레드 어디에서도 호출해서는 안 됨.
    # 익스큐터에서 호출하면 이 문제를 해결할 수 있음.
    time.sleep(0.5)
    print(f"{time.ctime()} Hello from a thread!")


loop = asyncio.get_event_loop()
task = loop.create_task(main())

# loop.run_in_executor(None, blocking)
loop.run_until_complete(task)

pending = asyncio.all_tasks(loop=loop)
for task in pending:
    task.cancel()

group = asyncio.gather(*pending, return_exceptions=True)
loop.run_until_complete(group)
loop.close()
