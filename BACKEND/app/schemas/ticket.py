import json
from pydantic import BaseModel, field_validator, model_validator

from datetime import datetime
from typing import Optional, overload, Dict, Union, Any, List, ClassVar


# class IssueType(BaseModel): #WT
#
#     __issuetypes__ = {
#         'service': 10201,
#         10201: ''
#     }
#     @overload
#     def __getattr__(self, item):
#         if item in self.__issuetypes__:
#             return self.__issuetypes__[item]
#
# class ServiceType(BaseModel): #WT
#     __servicetypes__ = {
#         'Не указан' : 0
#     }
#
#
# class StatusType:
#
#     status = {
#         0: 'Не создан',
#         10609: 'Открыт',
#         10611: 'Назначен',
#     }
#     id = {
#         'Не создан': 0,
#         'Открыт': 10609,
#         'Назначен': 10611,
#     }
#
#     def __init__(self, key: str | int | None):
#         key = 0 if key is None else key
#         if not isinstance(key, str):
#             self.value = self.status[key]
#             self.id = key
#         elif isinstance(key, int):
#             self.id = key
#             self.value = self.status[key]
#         else:
#             raise ValueError(f'Недопустимое знаечение: {key}')
#

class StatusType:
    status: ClassVar[dict[int, str]] = {
        0: 'Не создан',
        10609: 'Открыт',
        10611: 'Назначен',
    }
    id_map: ClassVar[dict[str, int]] = {v: k for k, v in status.items()}

    def __init__(self, key: int | str | None):
        if key is None:
            key = 0
        if isinstance(key, int):
            if key not in self.status:
                raise ValueError(f"Неизвестный статус: {key}")
            self.id = key
            self.value = self.status[key]
        elif isinstance(key, str):
            if key not in self.id_map:
                raise ValueError(f"Неизвестный статус: {key}")
            self.value = key
            self.id = self.id_map[key]
        else:
            raise ValueError(f'Недопустимое значение: {key}')

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'StatusType(id={self.id}, value="{self.value}")'

    def dict(self):
        return {"id": self.id, "value": self.value}

    def json(self):
        return json.dumps(self.dict())

class TicketCreate(BaseModel):
    tg_user_id: int
    issue_type: str
    title: str
    description: str
    service: str | int = 0



class TicketResponse(BaseModel):
    id: Optional[int]
    tg_user_id: int
    jsd_id: str
    issue_type: int
    title: Optional[str]
    description: Optional[str]
    status: StatusType = StatusType(0)
    service: int = 0
    comments: List[Dict[str, Any]] = list

    @field_validator('status', mode='before')
    def v_status(cls, value):
        try:
            value = int(value)
        except:
            pass
        return value if isinstance(value, StatusType) else StatusType(value)

    class Config: #!
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {
            StatusType: lambda v: v.dict()
        }

class GetTicketResponse(BaseModel):
    status: str
    data: TicketResponse
