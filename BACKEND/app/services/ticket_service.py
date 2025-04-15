from schemas.exceptions import TicketCreationError, TicketNotFoundError
from schemas.ticket import TicketCreate, TicketResponse
from utils.database import get_uow, UnitOfWork
from services.jira_service import JiraService
from fastapi import Depends
from utils import set_logger_filename



class TicketService:
    def __init__(self, jira_service: JiraService, uow: UnitOfWork = Depends(get_uow)):
        self.uow = uow
        self.jira_service = jira_service
        self.logger = set_logger_filename('TICKET_SERVICE')

    async def create_ticket(self, ticket_data: TicketCreate) -> TicketResponse:
        """
        Создает тикет в Jira, DB и Redis в транзакционном режиме.
        """
        async with self.uow:
            try:
                # 1. Создание в Jira
                jira_ticket = await self._create_jira_ticket(ticket_data)

                # 2. Сохранение в БД
                db_ticket = await self._save_to_database(jira_ticket)

                # 3. Кеширование в Redis
                await self._cache_to_redis(db_ticket)

                return db_ticket

            except Exception as e:
                self.logger.error(f"Ticket creation failed: {e}")
                await self.uow.session.rollback()
                raise TicketCreationError(f"Failed to create ticket: {str(e)}")

    async def get_ticket(self, ticket_id: int) -> TicketResponse:
        """Получает тикет из базы данных"""
        async with self.uow:
            ticket = await self.uow.ticket_repository.get_by_id(ticket_id)
            if not ticket:
                raise TicketNotFoundError(f"Ticket {ticket_id} not found")
            return TicketResponse.model_validate(ticket)

    async def _create_jira_ticket(self, ticket_data: TicketCreate) -> TicketResponse:
        """Создает тикет в Jira"""
        try:
            ticket = await self.jira_service.create_issue(ticket_data)
            self.logger.debug(f"Jira ticket created: {ticket.jsd_id}")
            return ticket
        except Exception as e:
            self.logger.error(f"Jira ticket creation failed: {e}")
            raise

    async def _save_to_database(self, ticket: TicketResponse) -> TicketResponse:
        """Сохраняет тикет в базу данных"""
        try:

            user = await self.uow.user_repository.get_user(ticket.tg_user_id)
            if not user:
                raise ValueError("User not found")


            db_ticket = await self.uow.ticket_repository.create(ticket)
            if not db_ticket:
                raise ValueError("Failed to save ticket to database")

            return TicketResponse.model_validate(db_ticket)
        except Exception as e:
            self.logger.error(f"Database save failed: {e}")
            raise

    async def _cache_to_redis(self, ticket: TicketResponse) -> None:
        """Кеширует тикет в Redis"""
        try:
            user = await self.uow.user_repository.get_user(ticket.tg_user_id)
            if not user:
                raise ValueError("User not found for Redis caching")

            success = await self.uow.redis_repository.add_ticket(
                tg_user_id=user.tg_user_id,
                email=user.email,
                ticket=ticket
            )
            if not success:
                raise ValueError("Failed to cache ticket in Redis")

            self.logger.debug(f"Ticket cached in Redis: {ticket.jsd_id}")
        except Exception as e:
            self.logger.error(f"Redis caching failed: {e}")
            raise