from repositories.ticket_repository import TicketRepository
from schemas.ticket import TicketCreate, TicketResponse
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from services.jira_service import JiraService
from repositories.redis_repository import RedisRepository
from repositories.user_repository import UserRepository


class TicketService:
    def __init__(self, db: AsyncSession, jira_service: JiraService, redis_repository: RedisRepository):
        self.db = db
        self.jira_service = jira_service
        self.redis_repository = redis_repository

    async def create_ticket(self, ticket: TicketCreate) -> TicketResponse:
        """
        Создает тикет в Jira, DB, Redis.
        :param user:
        :param ticket:
        :return: TicketResponse
        """
        # Дико перегруженная функция нужно менять.
        # Обязательно проработать процесс логирования и фидбека по ошибкам

        ticket = await self.jira_service.create_issue(ticket)
        await TicketRepository.create_ticket(ticket, self.db)
        user = await UserRepository.get_user(self.db, ticket.tg_user_id)
        await self.redis_repository.add_ticket(tg_user_id=user.tg_user_id, email=user.email, ticket=ticket)

        return ticket

    async def get_ticket(self, ticket_id: int) -> TicketResponse:
        """
        Получение запроса из базы.
        :param ticket_id:
        :return:
        """
        # Будет работать вебхук, который будет записывать данные тикета в базу, этот метод будет получать их из базы
        ticket = await TicketRepository.get_ticket(ticket_id, self.db)
        if not ticket:
            raise ValueError("Ticket not found")
        return TicketResponse.model_validate(ticket)
