from pydantic import BaseModel

class Profile(BaseModel):
    full_name: str
    company: str
    position: str
    contacts: list

class User(BaseModel):
    tg_user_id: int
    email: str
    profile: Profile
