from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from models.user import User, Profile
from schemas.profile import User as UserSchema, Profile as ProfileSchema

class UserRepository:

    # @staticmethod
    # async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    #     """ Получение пользователя по email. """
    #     query = select(User).where(User.email == email)
    #     result = await session.execute(query)
    #     return result.scalars().first()

    @staticmethod
    async def get_user(session: AsyncSession, tg_user_id: int) -> User | None: # _by_tg_id
        """ Получение пользователя по Telegram ID. """
        query = select(User).where(User.tg_user_id == tg_user_id)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def create_user(session: AsyncSession, email: str, tg_user_id: int) -> User:
        """ Создание нового пользователя. """
        new_user = User(email=email, tg_user_id=tg_user_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @staticmethod
    async def update_user(session: AsyncSession, user: UserSchema) -> User | None:
        """Функция обновления профиля пользоввателя."""
        # 2 замечания:
        # 1 - форсированно меняет полностью весь профиль пользователя.
        # 2 - не поддерживает обновление имперических данных (данных пользователя, а не профиля)

        try:
            query = select(User).where(User.tg_user_id == user.tg_user_id).options(
                joinedload(User.profile)
            )
            res = await session.execute(query)
            db_user = res.scalars().first()

            if not db_user: return None

            if user.profile:
                db_user.profile = Profile(**user.profile.model_dump())
            else:
                db_user.profile = Profile(**user.profile.model_dump())

            await session.commit()
            return db_user

        except Exception as e:
            await session.rollback()
            raise e





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

