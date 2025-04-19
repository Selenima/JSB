from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message, TelegramObject
from cachetools import TTLCache

from services.auth_service import AuthService
from repositories.redis_repository import RedisRepository
from utils.auth_cache import *
from utils.blacklist import check_blacklist
from cfg import cfg

class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        if check_blacklist(event.from_user.id):
            await event.answer("Вы заброкированы как подозрительный пользователь. Обратитесь к администратору проекта.")
            return

        if check_starter(event.from_user.id):
            return await handler(event, data)

        if isinstance(event, Message) and event.text and event.text.startswith('/start'):
            return await handler(event, data)

        redis_rep = RedisRepository(cfg.get_redis_url())
        user_id = event.from_user.id

        if check_cache(user_id):
            return await handler(event, data)

        session = await redis_rep.get_session(tg_user_id=user_id)
        if not session:
            await event.answer("🔒 Требуется аутентификация. Используйте /start")
            return

        add_to_cache(user_id)
        data['session'] = session

        return await handler(event, data)
