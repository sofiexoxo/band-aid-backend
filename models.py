from pydantic import BaseModel
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