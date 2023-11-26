import asyncio
import time


async def main():
    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} GoodBye!")


# asyncio.run(main())

# ? asyncio.run(main()) 실행되는 과정

# 코루틴을 실행하기 위해 필요한 루프 인스턴스를 얻음
# 동일 스레드에서 호출하면 코드의 어느 부분에서 get_event_loop()를 호출하든 매번 똑같은 루프 인스턴스를 반환.
# asyncio API로 여러 개의 이벤트 루프나 스레드를 다를 수 있지만 대부분의 경우 하나의 메인 스레드만 사용함.
# async def 함수 내에서 호출하는 경우에는 asyncio.get_running_loop()를 호출해야 함.
loop = asyncio.get_event_loop()

# 이 문법을 호출하기 전까지 코루틴 함수는 실행되지 않음.
# 즉, create_task(coroutine)를 호출해서 루프에 코루틴을 스케줄링함.
# 매개 변수는 async def 함수 자체가 아니라 async def 함수를 호출하여 반환받은 결과.
# 반환받은 task 객체를 통해 작업의 상태를 모니터링할 수 있음. (아직 실행 중인지 혹은 완료되었는지)
# 코루틴 완료 후 코루틴이 반환한 값도 얻을 수 있음.
# task.cancel()을 호출하여 작업을 취소할 수도 있음.
task = loop.create_task(main())

# 호출을 통해 현재 스레드(보통은 메인 스레드)를 블로킹할 수 있음.
# run_until_complete()를 호출하면 매개변수로 전달했던 coroutine의 코루틴이 완료될 때까지 루프를 실행함.
# 루프가 실행되는 동안 스케줄링된 다른 작업들도 같이 실행됨.
# asyncio.run()도 내부에서 run_until_complete()를 호출하여 메인 스레드를 블로킹함.
loop.run_until_complete(task)
# process signal이나 loop.stop() 호출로 인한 루프 중지 등으로 'main' 내의 블로킹 상태가 풀린 후 (위의 코드에서 await asyncio.sleep(1.0)이 반환된 후)
# 아래 코드가 실행됨

pending = asyncio.all_tasks(loop=loop)
for task in pending:
    # 모든 태스크에게 취소 요청
    task.cancel()

group = asyncio.gather(*pending, return_exceptions=True)  # 아직 실행 중인 태스크 취합
loop.run_until_complete(group)  # 태스크들이 모두 종료 상태가 될 때까지 대기

# 정지된 루프에 대해 호출해야 함
# 루프의 모든 대기열을 비우고 executor를 종료시킴. 정지된 루프는 다시 실행될 수 있으나, 닫힌 루프는 완전히 끝난 것.
loop.close()

# 위의 모든 과정이 asyncio.run() 실행 시 수행됨.
