from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TicketCreate(BaseModel):
    tg_user_id: int
    title: str
    description: str

class TicketResponse(BaseModel):
    id: int
    issus_type: str
    jira_id: str | None = None
    title: str
    description: str
    status: str


    class Config: #!
        from_attributes = True