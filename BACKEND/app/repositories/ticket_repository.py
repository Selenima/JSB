from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.ticket import Ticket
from models.user import User
from schemas.ticket import TicketResponse

class TicketRepository:
    @staticmethod
    async def create_ticket(ticket_data: TicketResponse, session: AsyncSession) -> Ticket:
        """

        :param user:
        :param ticket_data:
        :param db:
        :return:
        """
        new_ticket = Ticket(
            tg_user_id=ticket_data.tg_user_id,
            jsd_id=ticket_data.jsd_id,
            issue_type=ticket_data.issue_type,
            title=ticket_data.title,
            description=ticket_data.description,
            status=ticket_data.status.id,
            service=ticket_data.service,
        )
        session.add(new_ticket)
        await session.commit()
        await session.refresh(new_ticket)
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

    @staticmethod
    async def update_ticket(ticket: Ticket, db: AsyncSession) -> Ticket | None:
        pass

