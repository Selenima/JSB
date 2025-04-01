from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_profile_keyboard():

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Edit profile"))
    return keyboard
