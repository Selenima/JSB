from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TicketCreate(BaseModel):
    title: str
    description: str

class TicketResponse(BaseModel):
    id: int
    jira_id: str | None = None
    title: str
    description: str
    status: str
    created_at: datetime

    class Config: #!
        from_attributes = True