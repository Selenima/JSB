import redis.asyncio as aioredis
import hashlib
import json
import time

class RedisRepository:

    def __init__(self, redis_url: str):

        self.redis = aioredis.from_url(redis_url, decode_responses=True)

    def hash_256(self, value):
        return hashlib.sha256(str(value).encode()).hexdigest()

    async def set_otp(self, tg_user_id: int, otp_code: str, expire_seconds: int = 300):
        """
        Хеширует tg_user_id и otp_code, сохраняет в Redis на 5 минут
        :param tg_user_id: H
        :param otp_code: H
        :param expire_seconds: TTL
        """

        session_key = self.hash_256(tg_user_id)
        otp_code = self.hash_256(otp_code)
        await self.redis.setex(session_key, expire_seconds, otp_code)

    async def verify_otp(self, tg_user_id: int, otp_code: str) -> bool:
        """
        ### Реплика функции, на данном этапе
        Проверяет код и удаляет его при успешном вводе.
        :param tg_user_id:
        :param otp_code:
        :return: Результат проверки совпадения кода.
        """

        user_key = self.hash_256(tg_user_id)
        stored_otp_code = await self.redis.get(user_key)

        if not stored_otp_code:
            return False

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
        session_data = json.dumps({"email": email, "expires_at": time.time() + expire_seconds}) # WT
        await self.redis.setex(session_key, expire_seconds, session_data)
        return session_key

    async def get_session(self, tg_user_id: int, email: str):
        """
        Получает данные пользователя Redis.
        :param tg_user_id:
        :param email:
        :return: Session data.
        """
        session_key = self.hash_256(f'{tg_user_id}{email}')
        session_data = await self.redis.get(session_key)

        return json.loads(session_data) if session_data else None
