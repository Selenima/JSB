from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.ticket import TicketCreate, TicketResponse, GetTicketResponse
#from utils.database import get_uow, UnitOfWork
from utils import set_logger_filename
from services import ticket_service

router = APIRouter(prefix="/tickets", tags=["tickets"])



@router.post("/", response_model=TicketResponse)
async def create_ticket(ticket_data: TicketCreate):
    """
    Создание новой заявки.
    :param ticket_data:
    :param db:
    :return: TicketResponse (serialize)
    """

    logger = set_logger_filename('TICKET_CREATING')
    logger.debug(f'ticket_data: {ticket_data.model_dump()}') #Временная опция на этапе тестов


    ticket = await ticket_service.create_ticket(ticket_data)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ticket creation failed')

    return GetTicketResponse(status='success', data=ticket)

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: int):
    """
    Получает заявку по идентификатору
    :param ticket_id:
    :param db:
    :return:
    """

    try:
        ticket = await ticket_service.get_ticket(ticket_id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    return GetTicketResponse(status='success', data=ticket)
