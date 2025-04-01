from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User

class UserRepository:

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
        """ Получение пользователя по email. """
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_user_by_tg_id(session: AsyncSession, tg_user_id: int) -> User | None:
        """ Получение пользователя по Telegram ID. """
        query = select(User).where(User.tg_user_id == tg_user_id)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def create_user(session: AsyncSession, email: str, tg_user_id: int) -> User:
        """ Создание нового пользователя. """
        new_user = User(email=email, tg_usцer_id=tg_user_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

