from aiogram import types, Router, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from models.ticket import Ticket

from app.keyboards.create_ticket import get_create_ticket_keyboard
from repositories.ticket_repository import TicketRepository
from repositories.user_repository import UserRepository

router = Router()

class CreateTicketStates(StatesGroup):
    title = State()
    description = State()
    attachments = State()

@router.message(Command('create_ticket'))
async def start_create_ticket(message: types.Message, state: FSMContext):
    await message.answer("Введите тему заявки:")
    await state.set_state(CreateTicketStates.title)

@router.message(CreateTicketStates.title)
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите описание заявки:")
    await state.set_state(CreateTicketStates.description)

@router.message(CreateTicketStates.description)
async def process_description(message: types.Message, state: FSMContext, user_repository: UserRepository, ticket_repository: TicketRepository):
    user_data = await state.get_data()
    user = await user_repository.get_user(message.from_user.id)
    ticket = Ticket(
        ticket_id="SD-21456", # stub
        user_id=user.user_id,
        title=user_data['title'],
        description=message.text,
        full_name=user.full_name,
        company=user.company,
        position=user.position,
        phone_number=user.phone_number,
    )

    await ticket_repository.create_ticket(ticket)
    await message.answer('Ticket created successfully.', reply_markup=get_create_ticket_keyboard())
    await state.clear()

def register_create_ticket_handlers(dp: Dispatcher):
    dp.include_router(router)
