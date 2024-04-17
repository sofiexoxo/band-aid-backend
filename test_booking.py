import pytest
from unittest.mock import AsyncMock
from repository.booking_repository import (
    create_booking,
    get_bookings_by_email,
    update_booking_date,
    delete_booking
)
from models import Booking

@pytest.fixture
def db_connection():
    return AsyncMock()

# Test for create_booking function
@pytest.mark.asyncio
async def test_create_booking(db_connection):
    # Prepare test data
    test_booking = Booking(name="John Doe", email="john@example.com", date="2024-04-20", band="Band Name")

    # Configure db_connection to have an asynchronous execute method
    db_connection.execute = AsyncMock()

    # Call the function being tested
    await create_booking(db_connection, test_booking)

    # Check if the correct query was executed
    db_connection.execute.assert_called_once_with(
        "INSERT INTO bookings (name, email, date, band) VALUES ($1, $2, $3, $4) RETURNING id, date, band",
        "John Doe",
        "john@example.com",
        "2024-04-20",
        "Band Name"
    )

# Test for update_booking_date function
@pytest.mark.asyncio
async def test_update_booking_date(db_connection):
    test_booking_id = 1
    new_date = "2024-05-20"

    # Configure db_connection to have an asynchronous execute method
    db_connection.execute = AsyncMock()

    # Call the function being tested
    await update_booking_date(db_connection, test_booking_id, new_date)

    # Check if the correct query was executed
    db_connection.execute.assert_called_once_with(
        "UPDATE bookings SET date = $1 WHERE id = $2",
        "2024-05-20",
        1
    )

# Test for delete_booking function
@pytest.mark.asyncio
async def test_delete_booking(db_connection):
    test_booking_id = 1

    # Configure db_connection to have an asynchronous execute method
    db_connection.execute = AsyncMock()

    # Call the function being tested
    await delete_booking(db_connection, test_booking_id)

    # Check if the correct query was executed
    db_connection.execute.assert_called_once_with(
        "DELETE FROM bookings WHERE id = $1",
        1
    )
