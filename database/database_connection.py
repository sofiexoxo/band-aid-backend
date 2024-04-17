import asyncpg
from asyncpg import Connection  # Add this import statement
from database.database_config import DATABASE_URL

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn

    async def connect(self) -> Connection:
        connection = await asyncpg.connect(self.dsn)  # Use self.dsn instead of DATABASE_URL
        try:
            return connection
        finally:
            await connection.close()

    async def close(self, connection: Connection):
        await connection.close()

    async def execute(self, query: str, *args):
        async with self.connect() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query: str, *args):
        async with self.connect() as connection:
            return await connection.fetch(query, *args)
