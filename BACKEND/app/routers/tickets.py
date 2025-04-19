from fastapi import APIRouter, Depends, status, HTTPException
from schemas.ticket import TicketCreate, TicketResponse, GetTicketResponse
from utils.database import get_uow_dep, UnitOfWork
from utils import set_logger_filename
from services.ticket_service import TicketService
from services import jira_service

router = APIRouter(prefix="/tickets", tags=["tickets"])



@router.post("/create", response_model=GetTicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket_data: TicketCreate, uow: UnitOfWork = Depends(get_uow_dep)):
    """
    Создание новой заявки.
    :param ticket_data:
    :param db:
    :return: TicketResponse (serialize)
    """

    logger = set_logger_filename('TICKET_CREATING')
    logger.debug(f'ticket_data: {ticket_data.model_dump()}') #Временная опция на этапе тестов

    ticket_service = TicketService(jira_service, uow)
    ticket = await ticket_service.create_ticket(ticket_data)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ticket creation failed')

    return GetTicketResponse(status='success', data=ticket)

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: int, uow: UnitOfWork = Depends(get_uow_dep)):
    """
    Получает заявку по ключу
    """
    ticket_service = TicketService(jira_service, uow)
    try:
        ticket = await ticket_service.get_ticket(ticket_id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    return GetTicketResponse(status='success', data=ticket)
