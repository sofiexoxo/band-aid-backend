from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
import jwt
import asyncpg

app = FastAPI()

DATABASE_URL = "postgresql://postgres:Schatje123@localhost:5432/band_aid"


async def get_database_connection():
    connection = await asyncpg.connect(DATABASE_URL)
    try:
        yield connection
    finally:
        await connection.close()

# Definieer de User-klasse
class User(BaseModel):
    email: str
    password: str

# Definieer de Booking-klasse
class Booking(BaseModel):
    name: str
    email: str
    date: str
    band: str

# CryptContext voor wachtwoord hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Geheime sleutel voor JWT-signering (moet veilig worden opgeslagen)
SECRET_KEY = "secretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Functie om wachtwoord te hashen
def hash_password(password: str):
    return pwd_context.hash(password)

# Functie om wachtwoord te verifieren
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Functie om gebruiker op te halen op basis van email
async def get_user(connection, email: str):
    query = "SELECT * FROM users WHERE email = $1"
    record = await connection.fetchrow(query, email)
    if record:
        return User(email=record['email'], password=record['password'])
    return None

# Functie om gebruiker op te slaan in de database
async def create_user(connection, user: User):
    query = "INSERT INTO users (email, password) VALUES ($1, $2)"
    await connection.execute(query, user.email, hash_password(user.password))

# Functie om JWT-token te maken
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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
    ]
    return bands
