
import asyncpg

from database.database_config import DATABASE_URL

async def get_database_connection():
    connection = await asyncpg.connect(DATABASE_URL)
    try:
        yield connection
    finally:
        await connection.close()
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
