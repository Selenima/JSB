from models.ticket import Ticket
from repositories.redis_repository import RedisRepository
from utils.baseAPIClient import BaseAPIClient
from utils import auto_logger

class TicketService(BaseAPIClient):

    def __init__(self, redis_repository: RedisRepository, backend_url: str, api_version: str):
        super().__init__(backend_url, api_version)
        self.redis_repository = redis_repository


    async def create_ticket(self, ticket: Ticket):
        """Отправляем запрос на создание тикета"""
        data = dict(
            tg_user_id=ticket.tg_user_id,
            issue_type=ticket.issue_type,
            title=ticket.title,
            description=ticket.description
        )
        resp = await self.post('tickets/create', json=data)
        if not resp:
            return None
        resp = resp.get('data')
        if not resp:
            return None

        ticket = Ticket(tg_user_id=resp.get('tg_user_id'))
        for field, value in resp.items():
            try:
                if field == 'status':
                    ticket.status.from_dict(value)
                    continue
                setattr(ticket, field, value)
            except AttributeError:
                auto_logger.warning(f'AttributeError: {field} not found in TicketService')
            except Exception as e:
                auto_logger.warning(f'SetAttrError: field: {field}, value: {value} Exception: {e}')
        return ticket

