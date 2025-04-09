import  aiohttp
from models.ticket import Ticket
from repositories.redis_repository import RedisRepository

class TicketService:

    def __init__(self, redis_repository: RedisRepository, backend_url: str):
        self.redis_rep = redis_repository
        self.backend_url = backend_url if backend_url.endswith("/") else backend_url + "/"

    async def create_ticket(self, ticket: Ticket):
        """Отправляем запрос на создание тикета"""
        async with aiohttp.ClientSession() as session:
            resp = await session.post(f'{self.backend_url}tickets/', data=ticket.model_dump())
            if resp.status != 200:
                return None

            ticket_json = await resp.json()

            return Ticket(**ticket_json)
