import asyncio
from typing import Awaitable

import aioredis
from aioredis import Redis


async def main():
    redis = await aioredis.from_url("redis://localhost:6379/0")
    keys = ["America", "Africa", "Europe", "Asia"]

    async for value in OneAtATime(redis, keys):
        print(value.decode())

    async for value in one_at_a_time(redis, keys):
        print(value.decode())


class OneAtATime:
    def __init__(self, redis: Redis, keys: list[str]) -> None:
        self.redis = redis
        self.keys = keys

    def __aiter__(self):
        self.ikeys = iter(self.keys)
        return self

    async def __anext__(self) -> Awaitable:
        try:
            k = next(self.ikeys)
        except StopIteration:
            raise StopAsyncIteration

        value = await self.redis.get(k)
        return value


async def one_at_a_time(redis: Redis, keys: list[str]):
    for k in keys:
        value = await redis.get(k)
        yield value


if __name__ == "__main__":
    asyncio.run(main())
