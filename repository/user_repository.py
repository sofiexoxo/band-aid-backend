
import asyncpg
import pytest
from unittest.mock import MagicMock

async def get_user(connection, email: str):
    query = "SELECT * FROM users WHERE email = $1"
    record = await connection.fetchrow(query, email)
    if record:
        return {"email": record['email'], "password": record['password']}
    return None

async def create_user(connection, user):
    query = "INSERT INTO users (email, password) VALUES ($1, $2)"
    await connection.execute(query, user.email, user.password)
