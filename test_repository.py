import pytest
from unittest.mock import MagicMock, AsyncMock
from repository.user_repository import (
    get_user,
    create_user,
    get_user_by_email,
    update_user_password,
    delete_user
)
from models import User


# Mock database connection fixture
@pytest.fixture
def db_connection():
    return AsyncMock()
# Test for get_user function
@pytest.mark.asyncio
async def test_get_user(db_connection):
    test_email = "test@example.com"
    test_record = {"email": "test@example.com", "password": "hashed_password"}
    
    # Configure db_connection to have an asynchronous fetchrow method
    async def fetchrow(query, email):
        return test_record
    db_connection.fetchrow = AsyncMock(side_effect=fetchrow)
    
    result = await get_user(db_connection, test_email)

    db_connection.fetchrow.assert_called_once_with("SELECT * FROM users WHERE email = $1", test_email)
    assert result == test_record

# Test for create_user function
@pytest.mark.asyncio
async def test_create_user(db_connection):
    # Prepare test data
    test_user = User(email="test@example.com", password="hashed_password")

    # Configure db_connection to have an asynchronous execute method
    db_connection.execute = AsyncMock()

    # Call the function being tested
    await create_user(db_connection, test_user)

    # Check if the correct query was executed
    db_connection.execute.assert_called_once_with(
        "INSERT INTO users (email, password) VALUES ($1, $2) RETURNING id, email",
        "test@example.com",
        "hashed_password"
    )
@pytest.mark.asyncio
async def test_update_user_password(db_connection):
    test_email = "test@example.com"
    new_password = "new_hashed_password"

    # Configure db_connection to have an asynchronous execute method
    db_connection.execute = AsyncMock()

    # Call the function being tested
    await update_user_password(db_connection, test_email, new_password)

    # Check if the correct query was executed
    db_connection.execute.assert_called_once_with(
        "UPDATE users SET password = $1 WHERE email = $2",
        new_password,
        test_email
    )

# Test for delete_user function
@pytest.mark.asyncio
async def test_delete_user(db_connection):
    test_email = "test@example.com"

    # Configure db_connection to have an asynchronous execute method
    db_connection.execute = AsyncMock()

    # Call the function being tested
    await delete_user(db_connection, test_email)

    # Check if the correct query was executed
    db_connection.execute.assert_called_once_with(
        "DELETE FROM users WHERE email = $1",
        test_email
    )
