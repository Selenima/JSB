# from aiogram import types, Router, Dispatcher
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.filters import Command
# from models.ticket import Ticket
#
# from app.keyboards.create_ticket import get_create_ticket_keyboard
# #from repositories.ticket_repository import TicketRepository
# #from repositories.user_repository import UserRepository
#
# router = Router()
#
#
#
# class CreateTicketStates(StatesGroup):
#     title = State()
#     description = State()
#     attachments = State()
#
#
# @router.message(Command('create_ticket'))
# async def start_create_ticket(message: types.Message, state: FSMContext):
#
#     await message.answer("Введите тему заявки:")
#     await state.set_state(CreateTicketStates.title)
#
# @router.message(CreateTicketStates.title)
# async def process_title(message: types.Message, state: FSMContext):
#     await state.update_data(title=message.text)
#     await message.answer("Введите описание заявки:")
#     await state.set_state(CreateTicketStates.description)
#
# @router.message(CreateTicketStates.description)
# async def process_description(message: types.Message, state: FSMContext): # user_repository: UserRepository, ticket_repository: TicketRepository
#     user_data = await state.get_data()
#     user = await user_repository.get_user(message.from_user.id)
#     ticket = Ticket(
#         ticket_id="SD-21456", # stub
#         user_id=user.user_id,
#         title=user_data['title'],
#         description=message.text,
#         full_name=user.full_name,
#         company=user.company,
#         position=user.position,
#         phone_number=user.phone_number,
#     )
#
#     await ticket_repository.create_ticket(ticket)
#     await message.answer('Ticket created successfully.', reply_markup=get_create_ticket_keyboard())
#     await state.clear()
#
# def register_create_ticket_handlers(dp: Dispatcher):
#     dp.include_router(router)

from aiogram import F, Router, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from typing import Optional

from models.ticket import Ticket
from keyboards.ticket import get_create_ticket_keyboard, get_create_ticket_text
from repositories.redis_repository import RedisRepository
from services.ticket_service import TicketService

from cfg import Config

router = Router()

class TicketState(StatesGroup):
    editing = State()
    editing_title = State()
    editing_desc = State()

@router.message(Command("create_ticket"))
async def create_ticket(message: Message, state: FSMContext):
    data = await state.get_data()
    new_ticket = Ticket(tg_user_id=message.from_user.id, status=0)

    txt = get_create_ticket_text(new_ticket)
    if data['bad_try']:
        txt = 'Для отправки заявки поля "Тема" и "Описание" должны быть заполнены.\n' + txt
    msg = await message.answer(txt, reply_markup=get_create_ticket_keyboard(new_ticket))

    await state.update_data(
        bad_try=False,
        ticket=new_ticket,
        menu_message_id=msg.message_id,
        chat_id=message.chat.id
    )

    await state.set_state(TicketState.editing)


@router.message(TicketState.editing, F.text.regexp(r'^Тема:.*'))
async def start_edit_title(message: Message, state: FSMContext):

    #data = await state.get_data()

    msg = await message.answer('Введите тему заявки:')

    await state.update_data(
        temp_message_id=msg.message_id,
        editing_field = "title"
    )
    await state.set_state(TicketState.editing_title)

@router.message(TicketState.editing_title)
async def process_title(message: Message, state: FSMContext):

    data = await state.get_data()
    ticket = data['ticket']

    await message.bot.delete_messages(message.chat.id, [message.message_id, data['menu_message_id'], data['temp_message_id']])

    ticket.title = message.text

    msg = await message.answer(get_create_ticket_text(ticket), reply_markup=get_create_ticket_keyboard(ticket))

    await state.update_data(
        ticket=ticket,
        menu_message_id=msg.message_id
    )

    await state.set_state(TicketState.editing)

@router.message(TicketState.editing, F.text.regexp(r'^Описание:.*$'))
async def start_edit_desc(message: Message, state: FSMContext):

    data = await state.get_data()

    msg = await message.answer('Подробно опишите проблему. Чем больше информации, связанной с заявкой вы предоставите, тем быстрее она будет решена.')

    await state.update_data(
        temp_message_id=msg.message_id,
        editing_field = "description"
    )

    await state.set_state(TicketState.editing_desc)


@router.message(TicketState.editing_desc)
async def process_desc(message: Message, state: FSMContext):

    data = await state.get_data()

    ticket: Ticket = data['ticket']

    await message.bot.delete_messages(message.chat.id, [message.message_id, data['menu_message_id'], data['temp_message_id']])

    ticket.description = message.text

    msg = await message.answer(get_create_ticket_text(ticket), reply_markup=get_create_ticket_keyboard(ticket))

    await state.update_data(
        ticket=ticket,
        menu_message_id=msg.message_id
    )

    await state.set_state(TicketState.editing)

@router.message(TicketState.editing, F.text.endswith('Отмена'))
async def cancelcall(message: Message, state: FSMContext):

    data = await state.get_data()

    await message.bot.delete_messages(message.chat.id, [message.message_id, data['temp_message_id']] if data['temp_message_id'] else [message.message_id,])

    await message.answer("Создание заявки отмнено.")
    await state.clear()

@router.message(TicketState.editing, F.text == "Отправить")
async def submit_ticket(message: Message, state: FSMContext, ticket_service: TicketService = F.ticket_service): #, redis_repository: RedisRepository = F.redis_repository
    data = await state.get_data()
    ticket: Ticket = data['ticket']

    if not ticket.title:
        await state.update_data(bad_try=True)
        return

    if not ticket.description:
        await state.update_data(bad_try=True)
        return

    ticket = await ticket_service.create_ticket(ticket)

    await message.bot.delete_message(message.chat.id, message.message_id)
    #await state.update_data(ticket=ticket)
    # Открываем пользьвателю мейн меню или данную задачу в режим отслеживания (меню отслеживания изменений по заявке).

def register_start_handlers(dp: Dispatcher, redis_repository, ticket_service):
    dp.include_router(router)

    dp['redis_repository'] = redis_repository
    dp['ticket_service'] = ticket_service