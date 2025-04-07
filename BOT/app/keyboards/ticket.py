from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from models.ticket import Ticket, StatusType


def get_create_ticket_keyboard(ticket: Ticket):

    keyboard = [
        KeyboardButton(text=f'Тема: {ticket.title if ticket.title else ""}'),
        KeyboardButton(text=f'Описание: {ticket.description if ticket.description else ""}'),
        [
            KeyboardButton(text='Отмена'),
            KeyboardButton(text='Отправить')
        ]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return keyboard

def get_create_ticket_text(ticket: Ticket):
    text = f"""
{ticket.status.messages}

{f'[{ticket.ticket_id}]' if ticket.ticket_id else ''}
Тема: {ticket.title if ticket.title else 'Не указана'}

Тип запроса: {'Обслуживание' if ticket.issue_type else ''}
Статус: {ticket.status}

Описание: {ticket.description if ticket.description else 'Не указано'}

    Чтобы оставить комментарий нажмите кнопку...
"""
    return text
