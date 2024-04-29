from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from dataclasses import dataclass
from database.database_config import DATABASE_URL, async_engine, AsyncSession, Base, SessionLocal as async_session
from database.database_connection import Database 
from service.security_service import hash_password, verify_password, create_access_token
from repository.user_repository import get_user, create_user
from models import User, Booking
import asyncio

app = FastAPI()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def getAsyncDb():
    return Database()
    
def db_dependency():
    return Depends(getAsyncDb)

@dataclass
class LoginResponse:
    access_token: str
    token_type: str = "bearer"


@app.get("/")
async def start():
    return {"message": " successful"}
# OAuth2 Password Flow voor gebruikersauthenticatie
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Endpoint voor inloggen en genereren van JWT-token
@app.post("/api/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db:Database = Depends(Database)) -> LoginResponse:
    user = await get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return LoginResponse(access_token)

# Endpoint voor registreren
@app.post("/api/register")
async def register(user: User, db: Database = Depends(getAsyncDb)):
    existing_user = await get_user(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    await create_user(db, User(email=user.email, password=hash_password(user.password)))
    return {"message": "Registration successful"}

# Endpoint voor uitloggen
@app.post("/api/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    return {"message": "Logout successful"}


# Endpoint voor boeken
@app.post("/api/bookingpage")
async def book(booking: Booking):
    # Hier zou je typisch de boekingsgegevens naar je database opslaan
    # Voor demonstratiedoeleinden geven we hier gewoon de boekingsgegevens terug
    return {"message": "Booking successful", "booking": booking.dict()}




#TABLE CREATION    
async def create_tables():
    async with async_engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)

 
 
async def startup_event():
    await create_tables()
    await asyncio.sleep(5)  # Wait for tables to be created before starting the application
 
# Register the startup event
app.add_event_handler("startup", startup_event)

