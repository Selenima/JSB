from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.ticket import TicketCreate, TicketResponse, GetTicketResponse
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
    ticket = await service.create_ticket(ticket_data)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ticket creation failed')

    return GetTicketResponse(status='success', data=ticket)

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: int, db: AsyncSession = Depends(get_db), superset: TicketServiceSuperset = Depends(TicketServiceSuperset)):
    """
    Получает заявку по идентификатору
    :param ticket_id:
    :param db:
    :return:
    """
    service = TicketService(db, superset.jira_service, superset.redis_repository)
    try:
        ticket = await service.get_ticket(ticket_id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    return GetTicketResponse(status='success', data=ticket)
