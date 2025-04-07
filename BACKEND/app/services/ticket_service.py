from repositories.ticket_repository import TicketRepository
from schemas.ticket import TicketCreate, TicketResponse
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User

class TicketService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_ticket(self, ticket: TicketCreate) -> TicketResponse:
        """

        :param user:
        :param ticket:
        :return:
        """
        ticket = await TicketRepository.create_ticket(ticket, self.db)
        return TicketResponse.model_validate(ticket)

    async def get_ticket(self, ticket_id: int) -> TicketResponse:
        """

        :param ticket_id:
        :return:
        """

        ticket = await TicketRepository.get_ticket(ticket_id, self.db)
        if not ticket:
            raise ValueError("Ticket not found")
        return TicketResponse.model_validate(ticket)
