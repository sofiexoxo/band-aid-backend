import asyncio
import asyncpg
from asyncpg import Connection
from database.database_config import DATABASE_URL  


class Database:
    def __init__(self, dsn: str = DATABASE_URL):    
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

    async def fetchrow(self, query: str, *args):
        async with self.connect() as connection:
            return await connection.fetchrow(query, *args)


async def main():
    # Initialize the Database object with the DATABASE_URL
    db = Database()

    # Example user registration
    email = "example@example.com"
    password = "example_password"

    try:
        # Register the user
        await db.register_user(email, password)
        print("User registered successfully!")
    except Exception as e:
        print(f"Failed to register user: {e}")

    # Retrieve user data (just for demonstration)
    user_data = await db.get_user(email)
    print("User data:", user_data)

    # Close the database connection
    await db.close()
