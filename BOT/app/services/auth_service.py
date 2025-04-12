import json
import secrets
import aiohttp
from pydantic import EmailStr

from repositories.redis_repository import RedisRepository
from models.user import User
from utils.baseAPIClient import BaseAPIClient


class AuthService(BaseAPIClient):
    '''Сервис аутентификации на уровне бота.
    Описаны 2 функции верификации OTP-кода. Одна через обращение к Backend API,
    вторая через обращение к Redis. Подразумевается на уровне архитектуры опрашивать Redis.
    HTTP версия существует для вариативности.'''

    def __init__(self, redis_repository: RedisRepository, backend_url: str, api_version: str):
        super().__init__(backend_url, api_version)
        self.redis_rep = redis_repository


    async def send_code(self, email, tg_user_id):
        """
        Создает запрос к Backend API. Точка входа в процедуру верификации.
        :param email:
        :param tg_user_id:
        :return:
        """

        data = dict(email=email, tg_user_id=tg_user_id)
        response = await self.post('auth/send-code', json=data)
        return response is not None

    async def verify_code_http(self, tg_user_id: int, code: str, email: EmailStr):
        """
        Функция проверки кода через обращение к Backend API.
        :param email:
        :param tg_user_id:
        :return: Ключ сессии или None
        """
        data = {'tg_user_id': tg_user_id, 'code': code, 'email': email}
        response = await self.post('auth/verify-code', json=data)
        data = response.get('data')
        session_key = data.get('session_key') if data else None
        return session_key

    async def verify_code_local(self, tg_user_id: int, code: str, email: EmailStr) -> bool:
        """
        Фнукция проверки кода через обращение к Redis.
        :param tg_user_id:
        :param code:
        :return: Ключ сессии или None
        """

        is_valid = await self.redis_rep.verify_otp(tg_user_id, code)
        if not is_valid:
            return False

        session_key = await self.redis_rep.create_session(tg_user_id, str(email))
        return session_key

    async def get_active_session(self, tg_user_id): #WT
        """
        Функция проверяет существует ли данный пользователь в базе и наличие активной сессии.
        :param tg_user_id:
        :param email:
        :return: Сессию или Пользователя
        """
        response = await self.get('/users/from-db', params=dict(tg_user_id=tg_user_id))

        if not response:
            return None

        user = User(**response)
        session = await self.redis_rep.get_session(user.tg_user_id, user.email)

        return session if session else user
