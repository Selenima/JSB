from pydantic import BaseModel

class Profile(BaseModel):
    full_name: str
    company: str
    position: str
    contacts: list

class User(BaseModel):
    tuser_id: int
    email: str
    profile: Profile

    class Config:
        from_attributes = True

