import asyncpg
from asyncpg import Connection

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn

    async def connect(self) -> Connection:
        return await asyncpg.connect(self.dsn)

    async def close(self, connection: Connection):
        await connection.close()

    async def execute(self, query: str, *args):
        async with self.connect() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query: str, *args):
        async with self.connect() as connection:
            return await connection.fetch(query, *args)
