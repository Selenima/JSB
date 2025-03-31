import secrets
import aiohttp
from repositories.user_repository import UserRepository
from repositories.redis_repository import RedisRepository


class AuthService:
    def __init__(self, user_repository: UserRepository, backend_url: str):
        self.user_repository = user_repository
        self.backend_url = backend_url if backend_url.endswith("/") else backend_url + "/"

    async def send_code(self, email, tg_user_id):
        async with aiohttp.ClientSession() as session:
            req = await session.get(f'{self.backend_url}/auth/send-code?email={email}&tg_user_id={tg_user_id}')
            if req.status == 200:
                return True
            return False

    async def verify_code(self, email, code):

        return code == "123456" # Redis hand func
