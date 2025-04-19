from pydantic import BaseModel
from datetime import datetime

class Profile(BaseModel):
    full_name: str | None = None
    company: str | None = None
    position: str | None = None
    contacts: list | None = None

class User(BaseModel):
    id: int
    tg_user_id: int
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    profile: Profile | None = None

    class Config:
        from_attributes = True

