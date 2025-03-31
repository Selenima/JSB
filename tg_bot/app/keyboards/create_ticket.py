from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_create_ticket_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Добавить вложение"))
    keyboard.add(KeyboardButton("Отправить заявку"))