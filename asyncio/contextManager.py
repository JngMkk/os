class Connection:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.conn = None

    # 동기 컨텍스트 관리자를 위한 특별 메서드인 __enter__() 대신, __aenter__()라는 새로운 특별 메서드를 사용
    async def __aenter__(self):
        self.conn = await self.get_conn()
        return self.conn

    # __exit__() 대신 __aexit__()을 사용.
    # 매개변수는 __exit__()와 동일하고, 컨텍스트 관리자의 본문에서 예외가 발생하는 경우 호출됨.
    async def __aexit__(self):
        if self.conn is not None:
            await self.conn.close()
        else:
            raise

    async def get_conn(self):
        return ...


async def main():
    async with Connection("localhost", 9001) as conn:
        ...
