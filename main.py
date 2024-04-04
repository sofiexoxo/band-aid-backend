from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt


app = FastAPI()
users_db = [
    User(email="user1@example.com", password="password1"),
    User(email="user2@example.com", password="password2"),
    User(email="user3@example.com", password="password3")]

class User(BaseModel):
    email: str
    password: str

class Booking(BaseModel):
    name: str
    email: str
    date: str
    band: str
# CryptContext voor wachtwoord hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Geheime sleutel voor JWT-signering (moet veilig worden opgeslagen)
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
#om ww te hashen
def hash_password(password: str):
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
def get_user(email: str):
    for user in users_db:
        if user.email == email:
            return user
    return None

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

@app.post("/login")
async def login(user: User):
    if user.username not in db_users or db_users[user.username] != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}

@app.post("/register")
async def register(user: User):
    if get.user(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = hash_password(user.password)
    user_db.append(user)
    return {"message": "Registration successful"}

#route voor inloggen en genereren van jwt-token
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["email"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


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
