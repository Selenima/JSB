from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.ticket import Ticket
from models.user import User
from schemas.ticket import TicketCreate

class TicketRepository:
    @staticmethod
    async def create_ticket(user: User, ticket_data: TicketCreate, db: AsyncSession) -> Ticket:
        """

        :param user:
        :param ticket_data:
        :param db:
        :return:
        """
        new_ticket = Ticket(user_id=user.id, **ticket_data.model_dump())
        db.add(new_ticket)
        await db.commit()
        await db.refresh(new_ticket)
        return new_ticket

    @staticmethod
    async def get_ticket(ticket_id: int, db: AsyncSession) -> Optional[Ticket]:
        """

        :param ticket_id:
        :param db:
        :return:
        """
        result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
        return result.scalars().first()


