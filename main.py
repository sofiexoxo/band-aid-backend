from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
db_users = {}

class User(BaseModel):
    email: str
    password: str
class Booking(BaseModel):
    name: str
    email: str
    date: str
    band: str

@app.post("/login")
async def login(user: User):
    if user.username not in db_users or db_users[user.username] != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}

@app.post("/register")
async def register(user: User):
    if user.username in db_users:
        raise HTTPException(status_code=400, detail="Username already exists")
    db_users[user.username] = user.password
    return {"message": "Registration successful"}
@app.post("/book")
async def book(booking: Booking):
    # Here you would typically save the booking data to your database
    # For demonstration purposes, we'll just return the booking data
    return {"message": "Booking successful", "booking": booking.dict()}
@app.get("/bands")
async def get_bands():
    # Here you can retrieve bands from your database or any other data source
    bands = [
        {"name": "BandRockers", "genre": "Rock"},
        {"name": "GhostRockers", "genre": "Rock"},
        {"name": "Karikatura Reggae Fusion Band", "genre": "Reggae"},
        # Add more bands as needed
    ]
    return bands
