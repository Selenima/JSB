from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from schemas.ticket import TicketCreate, TicketResponse
from utils.database import get_db
from services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/", response_model=TicketResponse)
async def create_ticket(ticket_data: TicketCreate, db: AsyncSession = Depends(get_db)):
    """
    Создание новой заявки.
    :param ticket_data:
    :param user:
    :param db:
    :return:
    """
    service = TicketService(db)
    return await service.create_ticket(ticket_data)

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получает заявку по идентификатору
    :param ticket_id:
    :param db:
    :return:
    """
    service = TicketService(db)
    return await service.get_ticket(ticket_id)
