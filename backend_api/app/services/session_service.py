from repositories.redis_repository import RedisRepository

class SessionService:

    def __init__(self, redis_rep: RedisRepository):
        self.redis_rep = redis_rep

    async def create_session(self, tg_user_id: int, email: str):
        """
        Создает сессию пользователя в Redis после успешной проверки OTP
        :param tg_user_id:
        :param email:
        :return: Session key
        """
        return await self.redis_rep.create_session(tg_user_id, email)

    async def get_session(self, tg_user_id: int, email: str):
        """
        Возвращает данные сессии пользователя
        :param tg_user_id:
        :param email:
        :return: Session data
        """
        return await self.redis_rep.get_session(tg_user_id, email)
