from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.ticket import TicketCreate, TicketResponse
from utils.database import get_db
from services.ticket_service import TicketService
from models.superset import TicketServiceSuperset

router = APIRouter(prefix="/tickets", tags=["tickets"])



@router.post("/", response_model=TicketResponse)
async def create_ticket(ticket_data: TicketCreate, db: AsyncSession = Depends(get_db), superset: TicketServiceSuperset = Depends(TicketServiceSuperset)):
    """
    Создание новой заявки.
    :param ticket_data:
    :param db:
    :return: TicketResponse (serialize)
    """
    service = TicketService(db, superset.jira_service, superset.redis_repository)
    return await service.create_ticket(ticket_data)

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: int, db: AsyncSession = Depends(get_db), superset: TicketServiceSuperset = Depends(TicketServiceSuperset)):
    """
    Получает заявку по идентификатору
    :param ticket_id:
    :param db:
    :return:
    """
    service = TicketService(db, superset.jira_service, superset.redis_repository)
    return await service.get_ticket(ticket_id)
