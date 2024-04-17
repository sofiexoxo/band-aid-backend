import pytest
from unittest.mock import MagicMock, patch
from repository.user_repository import get_user, create_user

from unittest.mock import AsyncMock

from types import SimpleNamespace
from models import User

@pytest.fixture
def connection_mock():
    return MagicMock()

# Test for get_user function
@pytest.mark.asyncio
async def test_get_user(connection_mock):
    test_email = "test@example.com"
    test_record = {"email": "test@example.com", "password": "hashed_password"}
    
    # Configure connection_mock to have an asynchronous fetchrow method
    async def fetchrow(query, email):
        return test_record
    connection_mock.fetchrow = MagicMock(side_effect=fetchrow)
    
    result = await get_user(connection_mock, test_email)

    connection_mock.fetchrow.assert_called_once_with("SELECT * FROM users WHERE email = $1", test_email)
    assert result == test_record


# Test for create_user function
@pytest.mark.asyncio
async def test_create_user(connection_mock):
    # Prepare test data
    test_user = SimpleNamespace(email="test@example.com", password="hashed_password")

    # Configure connection_mock to have an asynchronous execute method
    connection_mock.execute = AsyncMock()

    # Call the function being tested
    await create_user(connection_mock, test_user)

    # Check if the correct query was executed
    connection_mock.execute.assert_called_once_with(
        "INSERT INTO users (email, password) VALUES ($1, $2) RETURNING id, email",
        "test@example.com",
        "hashed_password"
    )
@pytest.fixture(autouse=True)
async def close_connection(connection_mock):
    yield
    if not connection_mock.closed:
        await connection_mock.close()
