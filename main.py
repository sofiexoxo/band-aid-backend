from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
import jwt
import asyncpg

app = FastAPI()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.get("/")
async def start():
    return {"message": " successful"}
# OAuth2 Password Flow voor gebruikersauthenticatie
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Endpoint voor inloggen en genereren van JWT-token
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), connection = Depends(get_database_connection)):
    user = await get_user(connection, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint voor registreren
@app.post("/register")
async def register(user: User, connection = Depends(get_database_connection)):
    existing_user = await get_user(connection, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    await create_user(connection, User(email=user.email, password=user.password))
    return {"message": "Registration successful"}

# Endpoint voor uitloggen
@app.post("/logout")
async def logout():
    return {"message": "Logout successful"}

# Endpoint voor boeken
@app.post("/book")
async def book(booking: Booking):
    # Hier zou je typisch de boekingsgegevens naar je database opslaan
    # Voor demonstratiedoeleinden geven we hier gewoon de boekingsgegevens terug
    return {"message": "Booking successful", "booking": booking.dict()}

# Endpoint voor ophalen van bands
@app.get("/bands")
async def get_bands():
    bands = [
        {"name": "BandRockers", "genre": "Rock"},
        {"name": "GhostRockers", "genre": "Rock"},
        {"name": "Karikatura Reggae Fusion Band", "genre": "Reggae"},
        {"name": "Festi", "genre": "Blues"},
        {"name": "Fusion Band", "genre": "Fusion music"},
        {"name": "Catastrophe", "genre": "Reggae"},
        {"name": "Outlanders", "genre": "POP"},
        {"name": "ReACT", "genre": "jazz"},
        {"name": "LAUnch", "genre": "Reggae"},
    ]
    return bands
