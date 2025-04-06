from typing import Optional
from .user import Profile
from pydantic import BaseModel


class IssueType(BaseModel):

    __issuetypes__ = {
        'service': 10201
    }

class Ticket(BaseModel):
    ticket_id: str
    issue_type: IssueType | str = IssueType.service
    tg_user_id: int
    title: str
    description: str
    attachments: Optional[str] = None
