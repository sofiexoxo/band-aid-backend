
from pydantic import BaseModel

class UserSchema(BaseModel):
    email: str

class BookingSchema(BaseModel):
    name: str
    email: str
    date: str
    band: str
