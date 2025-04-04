# from models.user import User
# from repositories.user_repository import UserRepository
# from utils.database import get_db
#
# class ProfileService:
#     def __init__(self, user_repository: UserRepository):
#         self.user_repository = user_repository
#
#     async def get_profile(self, user_id: int) -> User:
#         """
#         Получение данных профиля.
#         :param user_id: ID пользователя.
#         :return: Данные профиля или None.
#         """
#         async with get_db() as session:
#             res = await self.user_repository.get_user_by_tg_id(session, user_id)
#             return res if res else None
#
#     # async def update_profile(self, user_id: int, profile_data: dict):
#     #     """
#     #     Обновление данных профиля.
#     #     :param user_id: ID пользователя.
#     #     :param profile_data: Новые данные профиля.
#     #     """
#     #     await self.user_repository.update_user(user_id, profile_data)

