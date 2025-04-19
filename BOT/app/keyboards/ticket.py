from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from models.ticket import Ticket, StatusType


def get_create_ticket_keyboard(ticket: Ticket):

    keyboard = [
        [KeyboardButton(text=f'Тема: {ticket.title if ticket.title else ""}')],
        [KeyboardButton(text=f'Описание: {ticket.description if ticket.description else ""}')],
        [
            KeyboardButton(text='Отмена'),
            KeyboardButton(text='Отправить')
        ]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return keyboard

def get_create_ticket_text(ticket: Ticket):

    text = f"""
    {ticket.status.message}
{f'[{ticket.jsd_id}]' if ticket.jsd_id else ''}
<b>Тема:</b> {ticket.title if ticket.title else 'Не указана'}

<b>Тип запроса:</b> {'Обслуживание' if ticket.issue_type else 'Обслуживание'} 
<b>Статус:</b> {ticket.status.value}

<b>Описание:</b> {ticket.description if ticket.description else 'Не указано'}

    {'Чтобы оставить комментарий нажмите кнопку...' if ticket.jsd_id else ''}
"""
    return text
