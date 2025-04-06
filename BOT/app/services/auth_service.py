import json
import secrets
import aiohttp
from pydantic import EmailStr

from repositories.redis_repository import RedisRepository
from models.user import User


class AuthService:
    '''Сервис аутентификации на уровне бота.
    Описаны 2 функции верификации OTP-кода. Одна через обращение к Backend API,
    вторая через обращение к Redis. Подразумевается на уровне архитектуры опрашивать Redis.
    HTTP версия существует для вариативности.'''

    def __init__(self, redis_repository: RedisRepository, backend_url: str):
        self.redis_rep = redis_repository
        self.backend_url = backend_url if backend_url.endswith("/") else backend_url + "/"

    async def send_code(self, email, tg_user_id):
        """
        Создает запрос к Backend API. Точка входа в процедуру верификации.
        :param email:
        :param tg_user_id:
        :return:
        """
        async with aiohttp.ClientSession() as session:
            req = await session.get(f'{self.backend_url}/auth/send-code?email={email}&tg_user_id={tg_user_id}')
            if req.status == 200: # *Обработчик*
                return True
            return False

    async def verify_code_http(self, tg_user_id: int, code: str, email: EmailStr):
        """
        Функция проверки кода через обращение к Backend API.
        :param email:
        :param tg_user_id:
        :return: Ключ сессии или None
        """
        data = {'tg_user_id': tg_user_id, 'code': code, 'email': email}
        async with aiohttp.ClientSession() as session:
            req = await session.post(f'{self.backend_url}/auth/verify-code', data=data)
            if req.status == 200: # *Обработчик*
                resp = await req.json()
                return resp['session_key']
            return None

    async def verify_code_local(self, tg_user_id: int, code: str, email: EmailStr) -> bool:
        """
        Фнукция проверки кода через обращение к Redis.
        :param tg_user_id:
        :param code:
        :return: Ключ сессии или None
        """

        is_valid = await self.redis_rep.verify_otp(tg_user_id, code)
        if not is_valid:
            return None

        session_key = await self.redis_rep.create_session(tg_user_id, email)
        return session_key

    async def get_active_session(self, tg_user_id):
        """
        Функция проверяет существует ли данный пользователь в базе и наличие активной сессии.
        :param tg_user_id:
        :param email:
        :return: Сессию или None
        """
        async with aiohttp.ClientSession() as http_session:
            req = await http_session.get(f'{self.backend_url}/profile?tg_user_id={tg_user_id}')
            if req.status == 200:
                resp = await req.json()
                user = User(**resp) #!!!!

                session = await self.redis_rep.get_session(user.tg_user_id, user.email)

                return session if session else user
            return None
