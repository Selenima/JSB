from aiogram import Router
from aiogram import types, Dispatcher
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

from models.user import User
from services.auth_service import AuthService
from utils.blacklist import add_blacklist
from utils.auth_cache import starter, del_starter

router = Router()

class AuthStates(StatesGroup):
    email = State()
    code_ = State()
    success = State()

@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext, auth_service: AuthService = F.auth_service):

    count = (await state.get_data()).get('count')
    if not count:
        await state.update_data(count=5)
    elif count < 1:
        await add_blacklist(message.from_user.id)
        return

    session = await auth_service.get_active_session(message.from_user.id)

    if not session:
        await message.answer("Напишите адрес вашей электронной почты.")
        starter(message.from_user.id)
        await state.set_state(AuthStates.email)
    elif session and isinstance(session, User):
        await state.update_data(email=session.email)
        await state.set_state(AuthStates.code_)
    else:
        await state.set_state(AuthStates.success)

@router.message(AuthStates.email)
async def process_email(message: types.Message, state: FSMContext, auth_service: AuthService = F.auth_service):

    user_id = message.from_user.id

    data = await state.get_data()
    email = data.get("email")
    if email:
        await state.set_state(AuthStates.code_)
        return

    email = message.text.strip()
    # validation email func
    await state.update_data(email=email)
    await auth_service.send_code(email, user_id)
    await message.answer("Вам на почту направлено письмо с кодом. Напишите код из письма.")
    await state.set_state(AuthStates.code_)

@router.message(AuthStates.code_)
async def process_code(message: types.Message, state: FSMContext, auth_service: AuthService = F.auth_service):

    user_id = message.from_user.id
    code = message.text.strip()
    data = await state.get_data()
    # validation code func

    if await auth_service.verify_code_http(user_id, code, data.get("email")):
        await message.answer("Вы можете создать заявку с помощью команды /create_ticket")
        await state.clear()
        del_starter(message.from_user.id)
    else:
        count = data.get("count")
        await message.answer(f"Неверный код подтверждения. (Попыток осталось: {count - 1})")
        await state.update_data(count=count-1)
        await state.set_state(AuthStates.email)

def register_start_handlers(dp: Dispatcher, auth_service):
    dp.include_router(router)
    dp['auth_service'] = auth_service
