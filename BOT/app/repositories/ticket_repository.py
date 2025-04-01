from models.ticket import Ticket

class TicketRepository:
    async def create_ticket(self, ticket: Ticket):
        # Base ticket creating
        print(f'Task created: {ticket.id}')
        return ticket
