import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from app.handlers import register_handlers

from repositories.user_repository import UserRepository
from services.auth_service import AuthService

from cfg import Config

TOKEN = Config.token

default = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=TOKEN, default=default)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

user_repository = UserRepository()
auth_service = AuthService(user_repository)

register_handlers(dp, auth_service)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    #???????
    asyncio.run(main())
