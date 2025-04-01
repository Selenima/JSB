import redis.asyncio as redis

class RedisClient:

    def __init__(self, url: str):
        """
        Инициализация клиента Redis.
        :param url: URL для подключения к Redis (например, redis://localhost:6379).
        """
        self.client = redis.from_url(url)

    async def set(self, key: str, value: str, ex: int = None):
        """
        Установка значения по ключу.
        :param key: Ключ.
        :param value: Значение.
        :param ex: Время жизни ключа в секундах (опционально).
        """
        await self.client.set(key, value, ex=ex)

    async def get(self, key: str) -> str:
        """
        Получение значения по ключу.
        :param key:
        :return: Значение или None
        """
        return await self.client.get(key)

    async def hset(self, key: str, field: str, value: str):
        """
        Установка значения в хэше.
        :param key: Ключ хэша.
        :param field: Поле в хэше.
        :param value: Значение.
        """
        await self.client.hset(key, field, value)

    async def hget(self, key: str, field: str) -> str:
        """
        Получение значения из хэша.
        :param key: Ключ хэша.
        :param field: Поле в хэше.
        :return: Значение или None.
        """
        return await self.client.hget(key, field)

    async def close(self):
        """
        Закрытие соединения с Redis.
        """
        await self.client.close()
