import redis.asyncio as aioredis
import hashlib
import json
import time

class RedisRepository:

    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url)

    def hash_256(self, value):
        return hashlib.sha256(str(value).encode()).hexdigest()

    async def verify_otp(self, tg_user_id: int, otp_code: str) -> bool:
        """
        Проверяет код и удаляет его при успешном вводе.
        :param tg_user_id:
        :param otp_code:
        :return: Результат проверки совпадения кода.
        """

        session_key = self.hash_256(tg_user_id)
        stored_otp_code = await self.redis.get(session_key)

        if not stored_otp_code:
            return False

        user_code_hash = self.hash_256(otp_code)

        if user_code_hash == stored_otp_code:
            await self.redis.delete(session_key)
            return True

        return False

