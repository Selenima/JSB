import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from app.handlers import register_handlers

from services.auth_service import AuthService
from services.ticket_service import TicketService
from repositories.redis_repository import RedisRepository

from cfg import cfg

TOKEN = cfg.token

default = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=TOKEN, default=default)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


redis_rep = RedisRepository(cfg.get_redis_url())
auth_service = AuthService(redis_rep, cfg.backend_url, 'v1')
ticket_service = TicketService(redis_rep, cfg.backend_url)

register_handlers(dp, auth_service, redis_rep, ticket_service)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    #???????
    asyncio.run(main())
