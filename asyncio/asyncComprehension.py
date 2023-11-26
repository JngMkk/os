import asyncio


async def doubler(n: int):
    for i in range(n):
        yield i, i * 2
        await asyncio.sleep(0.1)


async def comprehension():
    result = [x async for x in doubler(3)]
    print(result)

    result = {x: y async for x, y in doubler(3)}
    print(result)

    result = {x async for x in doubler(3)}
    print(result)


async def f(x):
    await asyncio.sleep(0.1)
    return x + 100


async def factory(n):
    for x in range(n):
        await asyncio.sleep(0.1)
        yield f, x


async def comprehension2():
    result = [await f(x) async for f, x in factory(3)]
    print(result)


if __name__ == "__main__":
    asyncio.run(comprehension())
    asyncio.run(comprehension2())
