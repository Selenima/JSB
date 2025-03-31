# import secrets
# from backend_api.utils.redisClient import RedisClient
#
# class AuthService:
#
#     def __init__(self, redis_client: RedisClient):
#         self.redis_client = redis_client
#
#     async def send_code(self, email: str) -> str:
#         """
#         Отправка кода подтверждения на почту
#         :param email:
#         :return: Сгенерированный код.
#         """
#         code = str(secrets.randbelow(1000000)).zfill(6)
#         await self.redis_client.set(f'email_code:{email}', code, ex=300)
#
#         # Логика отправки кода
#
#         print(f'Код для {email}: {code}')
#         return code
#
#     async def verify_code(self, email: str, code: str) -> bool:
#         """
#         Проверка кода подтверждения.
#         :param email:
#         :param code: Введенный код.
#         :return: Результат проверки соответствия.
#         """
#
#         stored_code = await self.redis_client.get(f'email_code:{email}')
#         return stored_code == code
#

import random
import string
from utils.smtp_client import send_email
from repositories.redis_repository import RedisRepository

class AuthService:

    def __init__(self, redis_rep: RedisRepository, smtp_sender: str):
        self.redis_rep = redis_rep
        self.smtp_sender = smtp_sender

    def generate_otp(self, length: int = 6) -> str:
        """
        Генерирует случайный 6-значный код.
        :param length:
        :return: Code
        """
        return ''.join(random.choices(string.digits, k=length))

    async def send_otp(self, email: str, tg_user_id: int):
        """

        :param email:
        :param tg_user_id:
        :return:
        """

        otp_code = self.generate_otp()
        subject = "Аутентификация в чат-боте"
        message = f'''Здравствуйте!
        С помощью вашего почтового ящика была совершена попытка авторизации в чат-боте ServiceDesk.
        Ваш код подтверждения {otp_code}.
        Код действует 5 минут. Никому его не сообщайте.'''

        await send_email(self.smtp_sender, email, subject, message)
        await self.redis_rep.set_opt(tg_user_id, otp_code)

        return {"message": "Код отправлен."} ##


