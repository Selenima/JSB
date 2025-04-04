from pydantic import BaseModel

class Profile(BaseModel):
    fullname: str
    company: str
    position: str
    contacts: list

class User(BaseModel):
    tg_user_id: int
    email: str
    profile: Profile | None = None
