import json
from typing import Optional, overload, Dict, Union, Any, List, ClassVar
from pydantic import BaseModel, field_validator


class IssueType(BaseModel): #WT

    __issuetypes__ = {
        'service': 10201
    }

class ServiceType(BaseModel): #WT
    __servicetypes__ = {
        'Не указан' : 0
    }

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
#     messages = {
#         'Не создан': 'Пожалуйста, заполните форму (Тему и описание)',
#         'Открыт': 'Заявка создана, специалист обработает ее в течение 10 минут.',
#         'Зарегистрирован': 'Ваша заявка зарегистрирована и скоро будет назначена на исполнителя.',
#         'Назначен': 'Ваша заявка назначена на специалиста (или группу специалистов).\nВ ближайшее время приступим к решению.',
#         'Принят': 'Ваша заявка принята исполнителем.',
#         'В работе': 'Исполнитель занимается вашей заявкой.',
#         'Уточнение': 'Исполнителю требуются уточнения от вас. Просьба ответить комментарием.',
#         # добавить ссылку на отправку комментария
#         'Приостановлена': 'Ваша заявка приостановлена.',
#         'Отклонена': 'Ваша заявка отклонена. Чтобы выяснить причину прочитайте комментарии.',
#         'Выполнена': 'Ваша заявка выполнена. Можете ознакомиться с решением ниже.',
#         'Переоткрыта': 'Ваша заявка переоткрыта.'
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
#         self.message = self.messages.get(self.value)

class StatusType:
    status: ClassVar[dict[int, str]] = {
        0: 'Не создан',
        10609: 'Открыт',
        10611: 'Назначен',
    }

    messages = {
        'Не создан': 'Пожалуйста, заполните форму (Тему и описание)',
        'Открыт': 'Заявка создана, специалист обработает ее в течение 10 минут.',
        'Зарегистрирован': 'Ваша заявка зарегистрирована и скоро будет назначена на исполнителя.',
        'Назначен': 'Ваша заявка назначена на специалиста (или группу специалистов).\nВ ближайшее время приступим к решению.',
        'Принят': 'Ваша заявка принята исполнителем.',
        'В работе': 'Исполнитель занимается вашей заявкой.',
        'Уточнение': 'Исполнителю требуются уточнения от вас. Просьба ответить комментарием.',
        # добавить ссылку на отправку комментария
        'Приостановлена': 'Ваша заявка приостановлена.',
        'Отклонена': 'Ваша заявка отклонена. Чтобы выяснить причину прочитайте комментарии.',
        'Выполнена': 'Ваша заявка выполнена. Можете ознакомиться с решением ниже.',
        'Переоткрыта': 'Ваша заявка переоткрыта.'
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
        self.message = self.messages.get(self.value)

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'StatusType(id={self.id}, value="{self.value}")'

    def dict(self):
        return {"id": self.id, "value": self.value, "message": self.message}

    def json(self):
        return json.dumps(self.dict())

    def from_dict(self, data: dict):
        self.id = data['id']
        self.value = data['value']
        self.message = self.messages.get(self.value)
        return self

class Ticket(BaseModel):
    id: int = None
    tg_user_id: int
    jsd_id: str = None
    issue_type: Union[int, str] = None
    title: str = None
    description: str = None
    status: StatusType = StatusType(0)
    service: Union[int, str] = None
    comments: List[Dict[str, Any]] = list

    @field_validator('status', mode='before')
    def v_status(cls, value):
        try:
            value = int(value)
        except:
            pass
        return value if isinstance(value, StatusType) else StatusType(value)

    class Config:  # !
        from_attributes = True
        arbitrary_types_allowed = True
        # json_encoders = {
        #     StatusType: lambda v: v.dict()
        # }