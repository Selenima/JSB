from models.user import User
from repositories.user_repository import UserRepository

class ProfileService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_profile(self, user_id: int) -> User:
        """
        Получение данных профиля.
        :param user_id: ID пользователя.
        :return: Данные профиля.
        """
        return await self.user_repository.get_user(user_id)

    async def update_profile(self, user_id: int, profile_data: dict):
        """
        Обновление данных профиля.
        :param user_id: ID пользователя.
        :param profile_data: Новые данные профиля.
        """
        await self.user_repository.update_user(user_id, profile_data)