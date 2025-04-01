from typing import Optional

from pydantic import BaseModel


class Ticket(BaseModel):
    ticket_id: str
    tuser_id: int
    title: str
    description: str
    full_name: str  # ФИО из профиля
    company: str  # Компания из профиля
    position: str  # Должность из профиля
    phone_number: str  # Телефон из профиля
    attachments: Optional[str] = None
