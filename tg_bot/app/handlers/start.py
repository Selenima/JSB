from aiogram import Router
from aiogram import types, Dispatcher
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

from services.auth_service import AuthService

router = Router()

class AuthStates(StatesGroup):
    email = State()
    code_ = State()

@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await message.answer("*Getting mail*")
    await state.set_state(AuthStates.email)

@router.message(AuthStates.email)
async def process_email(message: types.Message, state: FSMContext, auth_service: AuthService = F.auth_service):

    email = message.text
    # validation email func
    await state.update_data(email=email)
    await auth_service.send_code(email)
    await message.answer("*Sending code* + *Getting code*")
    await state.set_state(AuthStates.code_)

@router.message(AuthStates.code_)
async def process_code(message: types.Message, state: FSMContext, auth_service: AuthService = F.auth_service):

    code = message.text
    # validation code func
    user_data = await state.get_data()
    if await auth_service.verify_code(code, user_data):
        await message.answer("*Verifying*")
        await state.clear()
    else:
        await message.answer("*Wrong code*")
        # Comeback

def register_start_handlers(dp: Dispatcher, auth_service): # ? auth_service
    dp.include_router(router)
    dp['auth_service'] = auth_service
