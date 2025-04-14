from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from models.user import User, Profile
from schemas.profile import User as UserSchema, Profile as ProfileSchema
from utils import set_logger_filename
from typing import Optional
from schemas import exceptions

class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, tg_user_id: int) -> User | None: # _by_tg_id
        """ Получение пользователя по Telegram ID. """

        query = (
            select(User)
            .where(User.tg_user_id == tg_user_id)
            .options(joinedload(User.profile))
        )

        result = await self.session.execute(query)
        return result.scalars().first()

    async def create_user(self, email: str, tg_user_id: int) -> Optional[User]:
        """ Создание нового пользователя. """

        logger = set_logger_filename('USER_CREATING')
        existing_user = await self.get_user( tg_user_id)
        if existing_user:
            logger.info('User already exists')
            return existing_user

        #email_check

        new_user = User(email=email, tg_user_id=tg_user_id)
        try:
            self.session.add(new_user)
            await self.session.flush()
            await self.session.refresh(new_user)
            logger.debug(f'User created: {new_user.id}')
            return new_user
        except Exception as e:
            logger.error(f'User creating: {e}')
            await self.session.rollback()
            if "unique constraint" in str(e).lower():
                raise exceptions.DuplicateUserError('User already exists')
            raise

    async def update_user(self, user_data: UserSchema) -> User | None:
        """Функция обновления профиля пользоввателя."""

        logger = set_logger_filename('USER_UPDATING')

        try:
            user = await self.get_user(user_data.tg_user_id)
            if not user:
                raise exceptions.UserNotFoundError('User does not exist')

            if user_data.profile:
                if not user.profile:
                    user.profile = Profile()
                for field, value in user_data.profile.model_dump().items():
                    try:
                        setattr(user.profile, field, value)
                    except AttributeError as e:
                        logger.warning(f'AttributeError: {e}')

            await self.session.flush()
            return user

        except Exception as e:
            logger.error(f'User updating: {e}')
            await self.session.rollback()
            raise





    # @staticmethod
    # async def get_user_profile(session: AsyncSession, user_id: int) -> Profile | None:
    #     """ Получение профиля пользователя по ID пользователя. """
    #     query = select(Profile).where(Profile.tg_user_id == user_id)
    #     result = await session.execute(query)
    #     return result.scalars().first()
    #
    # @staticmethod
    # async def update_user_profile(session: AsyncSession, profile: Profile) -> Profile | None:
    #     """ Обновление профиля пользователя. """
    #     try:
    #         session.add(profile)
    #         await session.commit()
    #         await session.refresh(profile)
    #         return profile
    #     except Exception:
    #         await session.rollback()
    #         return None
    #
    # @staticmethod
    # async def create_user_profile(session: AsyncSession, tg_user_id: int, **kwargs) -> Profile:
    #     """ Создание профиля пользователя. """
    #     profile = Profile(tg_user_id=tg_user_id, **kwargs)
    #     session.add(profile)
    #     await session.commit()
    #     await session.refresh(profile)
    #     return profile

