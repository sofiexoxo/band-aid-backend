from models import Booking
from database.database_connection import Database
async def create_booking(db: Database, booking: Booking):
    query = "INSERT INTO bookings (name, email, date, band) VALUES ($1, $2, $3, $4) RETURNING id, date, band"
    return await db.execute(query, booking.name, booking.email, booking.date, booking.band)

async def get_bookings_by_email(db: Database, email: str):
    query = "SELECT * FROM bookings WHERE email = $1"
    return await db.fetch_all(query, email)

async def update_booking_date(db: Database, booking_id: int, new_date: str):
    query = "UPDATE bookings SET date = $1 WHERE id = $2"
    return await db.execute(query, new_date, booking_id)

async def delete_booking(db: Database, booking_id: int):
    query = "DELETE FROM bookings WHERE id = $1"
    return await db.execute(query, booking_id)