from typing import Optional, overload, Dict, Union, Any
from pydantic import BaseModel, field_validator


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

        self.message = self.messages[self.value]

class Ticket(BaseModel):
    tg_user_id: int
    jsd_id: str
    issue_type: str
    title: str
    description: str
    status: str
    service: Union[int, str]
    comments: Dict[str, Any] = dict

    # @field_validator('status', mode='before')
    # def v_status(cls, value):
    #     return value if isinstance(value, StatusType) else StatusType(value)
