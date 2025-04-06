import redis.asyncio as aioredis
import hashlib
import json
import time

from models.ticket import Ticket


class RedisRepository:

    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url)

    def hash_256(self, value):
        return hashlib.sha256(str(value).encode()).hexdigest()

    async def verify_otp(self, tg_user_id: int, otp_code: str):
        """
        Проверяет код и удаляет его при успешном вводе.
        :param tg_user_id:
        :param otp_code:
        :return: Результат проверки совпадения кода.
        """

        user_key = self.hash_256(tg_user_id)
        stored_otp_code = await self.redis.get(user_key)

        if not stored_otp_code:
            return 

        user_code_hash = self.hash_256(otp_code)

        if user_code_hash == stored_otp_code:
            await self.redis.delete(user_key)
            return True

        return False

    async def create_session(self, tg_user_id: int, email: str, expire_seconds: int = 2_592_000):
        """
        Создает сессию пользователя в Redis.
        :param tg_user_id: H
        :param email: H
        :param expire_seconds: TTL
        :return: Session key
        """
        session_key = self.hash_256(f'{tg_user_id}{email}')
        session_data = json.dumps({"email": email, "expires_at": time.time() + expire_seconds})  # WT
        await self.redis.setex(session_key, expire_seconds, session_data)
        return session_key

    async def get_session(self, tg_user_id: int, email: str):
        """
        Получает данные пользователя Redis.
        :param tg_user_id:
        :param email:
        :return: Датасет или None
        """
        session_key = self.hash_256(f'{tg_user_id}{email}')
        session_data = await self.redis.get(session_key)
        return json.loads(session_data) if session_data else None

    async def add_ticket(self, tg_user_id: int, ticket: Ticket):
        """

        :param tg_user_id:
        :param ticket:
        :return:
        """

        user_key = self.hash_256(tg_user_id)

        await self.redis.set(user_key, ticket.model_dump(), ex=2_592_000)

