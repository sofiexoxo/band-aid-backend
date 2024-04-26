import asyncpg
from asyncpg import Connection
from database.database_config import DATABASE_URL  

class Database:
    def __init__(self, dsn: str = DATABASE_URL): 
        self.dsn = dsn

    async def connect(self) -> Connection:
        connection = await asyncpg.connect(self.dsn)  
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

    async def get_user(self, email): 
        query = "SELECT * FROM users WHERE email = $1"
        async with self.connect() as connection:
            record = await connection.fetchrow(query, email)
            return record
