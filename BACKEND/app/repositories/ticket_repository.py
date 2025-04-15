from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.ticket import Ticket
from schemas.ticket import TicketResponse
from utils import set_logger_filename



class TicketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = set_logger_filename('TICKET_REPOSITORY')

    async def create(self, ticket_data: TicketResponse) -> Optional[Ticket]:
        """

        :param user:
        :param ticket_data:
        :param db:
        :return:
        """

        try:
            new_ticket = Ticket(
                tg_user_id=ticket_data.tg_user_id,
                jsd_id=ticket_data.jsd_id,
                issue_type=ticket_data.issue_type,
                title=ticket_data.title,
                description=ticket_data.description,
                status=int(ticket_data.status),
                service=ticket_data.service,
            )
        except:
            self.logger.exception('Ticket object creation failed. Incorrect ticket data!!!!')
            return None

        try:

            self.session.add(new_ticket)
            await self.session.commit()
            await self.session.refresh(new_ticket)
            self.logger.debug(f'New ticket added: {new_ticket.jsd_id}')
            return new_ticket

        except Exception as e:
            self.logger.error(f'Ticket adding failed: {e}')
            return None

    async def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        """

        :param ticket_id:
        :param db:
        :return:
        """
        try:
            result = await self.session.execute(
                select(Ticket).where(Ticket.id == ticket_id)
            )
            ticket = result.scalars().first()

            if ticket:
                self.logger.debug(f'Ticket found: {ticket.jsd_id}')
            else:
                self.logger.warning(f'Ticket {ticket_id} not found')

            return ticket

        except Exception as e:
            self.logger.error(f'Ticket retrieval failed: {e}')
            return None


    async def update_ticket(self, ticket: Ticket) -> Optional[Ticket]:
        """Обновляет существующий тикет"""
        try:
            await self.session.flush()
            await self.session.refresh(ticket)
            self.logger.debug(f'Ticket updated: {ticket.jsd_id}')
            return ticket

        except Exception as e:
            self.logger.error(f'Ticket update failed: {e}')
            await self.session.rollback()
            return None
