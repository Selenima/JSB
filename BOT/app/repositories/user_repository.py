from models.user import User

class UserRepository:
    async def get_user(self, tuser_id) -> User:
        # Заглушка для получения пользователя
        return User(
            tuser_id=tuser_id,
            email="user@romashka.ru",
            full_name="Иван Иванов",
            company="ООО Ромашка",
            position="Инженер",
            phone_number="+79991234567"
        )