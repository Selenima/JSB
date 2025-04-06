from pydantic import BaseModel

class Profile(BaseModel):
    full_name: str | None = None
    company: str | None = None
    position: str | None = None
    contacts: list | None = None

class User(BaseModel):
    tuser_id: int
    email: str
    profile: Profile | None = None

    class Config:
        from_attributes = True

