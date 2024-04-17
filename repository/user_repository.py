
import asyncpg
import pytest
from unittest.mock import MagicMock
from database.database_connection import Database
from models import User

async def fetchrow(query, email):
    return test_record

async def get_user(connection, email: str):
    query = "SELECT * FROM users WHERE email = $1"
    record = await connection.fetchrow(query, email)
    if record:
        return {"email": record['email'], "password": record['password']}
    return None

async def create_user(db: Database, user: User):
    query = "INSERT INTO users (email, password) VALUES ($1, $2) RETURNING id, email"
    return await db.execute(query, user.email, user.password)

async def get_user_by_email(db: Database, email: str):
    query = "SELECT * FROM users WHERE email = $1"
    return await db.fetch_one(query, email)


async def update_user_password(db: Database, email: str, new_password: str):
    query = "UPDATE users SET password = $1 WHERE email = $2"
    return await db.execute(query, new_password, email)

async def delete_user(db: Database, email: str):
    query = "DELETE FROM users WHERE email = $1"
    return await db.execute(query, email)
