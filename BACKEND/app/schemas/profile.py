from datetime import datetime

from pydantic import BaseModel

class Profile(BaseModel):
    tg_user_id: int
    fullname: str
    company: str
    position: str
    contacts: list

class User(BaseModel):
    id: int
    tg_user_id: int
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    profile: Profile | None = None
