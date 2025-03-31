from pydantic import BaseModel

class User(BaseModel):
    tuser_id: int
    email: str
    full_name: str
    company: str
    position: str
    phone_number: str


