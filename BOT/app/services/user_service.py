import aiohttp
from models.user import User

class UserService:

    def __init__(self, api_url):
        self.api_url = api_url

    async def get_user(self, tg_user_id):
        """Получает пользователя из бд"""
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.api_url}/user/from-db?tg_user_id={tg_user_id}')

            if resp.status != 200:
                return None

            return await resp.json()

    async def set_user(self, user: User):
        """Изменяет пользователя (профиль) в бд"""

        data = user.model_dump()

        async with aiohttp.ClientSession() as session:
            resp = await session.put(f'{self.api_url}/user/profile-update', data=data)
            if resp.status != 204:
                return None
        return user


