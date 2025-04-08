from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class IssueType(BaseModel): #WT

    __issuetypes__ = {
        'service': 10201
    }

class ServiceType(BaseModel): #WT
    __servicetypes__ = {
        'Не указан' : 0
    }

class StatusType:

    status = {
        0: 'Не создан',
        10611: 'Назначен',
    }
    id = {
        'Не создан': 0,
        'Назначен': 10611,
    }

    def __init__(self, key: str | int | None):
        key = 0 if key is None else key
        if not isinstance(key, str):
            self.value = self.status[key]
            self.id = key
        elif isinstance(key, int):
            self.id = key
            self.value = self.status[key]
        else:
            raise ValueError(f'Недопустимое знаечение: {key}')




class TicketCreate(BaseModel):
    tg_user_id: int
    title: str
    description: str

class TicketResponse(BaseModel):
    tg_user_id: int
    jsd_id: str = None
    issue_type: IssueType | str = IssueType.service
    title: str = None
    description: str = None
    status: StatusType
    service: str | int = 0
    comments: dict = dict

    @field_validator('status', mode='before')
    def v_status(cls, value):
        return value if isinstance(value, StatusType) else StatusType(value)

    class Config: #!
        from_attributes = True