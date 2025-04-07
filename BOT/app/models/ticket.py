from typing import Optional
from pydantic import BaseModel, field_validator


class IssueType(BaseModel):

    __issuetypes__ = {
        'service': 10201
    }

class ServiceType(BaseModel):
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
    ticket_id: str = None
    issue_type: IssueType | str = IssueType.service
    tg_user_id: int
    title: str = None
    description: str = None
    status: StatusType
    service: str | int = None

    @field_validator('status', mode='before')
    def v_status(cls, value):
        return value if isinstance(value, StatusType) else StatusType(value)
