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
from utils import auto_logger

router = Router()

class AuthStates(StatesGroup):
    email = State()
    code_ = State()
    success = State()

# @router.message(Command('start'))
# async def start(message: types.Message, state: FSMContext, auth_service: AuthService = F.auth_service):
#
#     count = (await state.get_data()).get('count')
#     if not count:
#         await state.update_data(count=5)
#     elif count < 1:
#         await add_blacklist(message.from_user.id)
#         auto_logger.info(f'User blacklisted by {message.from_user.id}.')
#         return
#
#     auto_logger.info(f'Started {message.from_user.id}')
#
#     session = await auth_service.get_active_session(message.from_user.id)
#     auto_logger.debug(f'Session/User: {session}')
#     if not session:
#         await message.answer("Напишите адрес вашей электронной почты.")
#         starter(message.from_user.id)
#         await state.set_state(AuthStates.email)
#     elif session and isinstance(session, User):
#         starter(message.from_user.id)
#         email = session.email
#         user_id = session.tg_user_id
#         stat = await auth_service.send_code(email, user_id)
#         if not stat:
#             await message.answer(
#                 'Не удалось отправить код на данный почтовый адрес. Пришлите корректный адрес и повторите попытку...')
#             await state.update_data(email=None)
#             auto_logger.warning(f'Bad email: {email}')# !!!!!!!!!!!!
#             await state.set_state(AuthStates.email)
#             return
#         await state.update_data(email=email)
#         await message.answer("Вам на почту направлено письмо с кодом. Напишите код из письма.")
#         await state.set_state(AuthStates.code_)
#     else:
#         await state.set_state(AuthStates.success)
@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext, auth_service: AuthService = F.auth_service):
    user_id = message.from_user.id
    state_data = await state.get_data()
    count = state_data.get('count', 5)

    if count < 1:
        await add_blacklist(user_id)
        auto_logger.info(f'User blacklisted: {user_id}')
        return

    await state.update_data(count=count)  # Если count уже был, ничего не меняется

    auto_logger.info(f'Started auth for user {user_id}')
    session_or_user = await auth_service.get_active_session(user_id)
    auto_logger.debug(f'Session/User: {session_or_user}')

    if session_or_user is None:
        # Пользователь не найден — просим email
        starter(user_id)
        await message.answer("Напишите адрес вашей электронной почты.")
        await state.set_state(AuthStates.email)

    elif isinstance(session_or_user, User):
        # Пользователь есть, но сессии нет — отправляем код
        user = session_or_user
        starter(user_id)
        success = await auth_service.send_code(user.email, user_id)

        if not success:
            await message.answer("Не удалось отправить код. Убедитесь в правильности email и попробуйте снова.")
            await state.update_data(email=None)
            auto_logger.warning(f'Bad email: {user.email}')
            await state.set_state(AuthStates.email)
            return

        await state.update_data(email=user.email)
        await message.answer("Вам на почту отправлен код. Введите его.")
        await state.set_state(AuthStates.code_)

    else:
        # Есть активная сессия — уже авторизован
        await state.clear()
        await message.answer('Вы уже авторизовны и можете пользоваться ботом.')


# @router.message(AuthStates.email)
# async def process_email(message: types.Message, state: FSMContext, auth_service: AuthService = F.auth_service):
#
#     user_id = message.from_user.id
#
#     data = await state.get_data()
#     email = data.get("email")
#     if not email:
#         email = message.text.strip()
#
#     await state.update_data(email=email)
#
#     auto_logger.info(f'Processing email: {message.from_user.id}')
#
#     stat = await auth_service.send_code(email, user_id)
#     if not stat:
#         await message.answer('Не удалось отправить код на данный почтовый адрес. Проверьте адрес и повторите попытку...')
#         await state.update_data(email=None)
#         auto_logger.warning(f'Bad email: {email}') #!!!!!!!!!!!!
#         return
#     await message.answer("Вам на почту направлено письмо с кодом. Напишите код из письма.")
#     await state.set_state(AuthStates.code_)
@router.message(AuthStates.email)
async def process_email(message: types.Message, state: FSMContext, auth_service: AuthService = F.auth_service):
    user_id = message.from_user.id
    email = message.text.strip()

    await state.update_data(email=email)
    auto_logger.info(f'Processing email for {user_id}')

    if await auth_service.send_code(email, user_id):
        await message.answer("Вам на почту отправлен код. Введите его.")
        await state.set_state(AuthStates.code_)
    else:
        await message.answer("Не удалось отправить код. Проверьте email и попробуйте снова.")
        await state.update_data(email=None)
        auto_logger.warning(f'Bad email: {email}')


# @router.message(AuthStates.code_)
# async def process_code(message: types.Message, state: FSMContext, auth_service: AuthService = F.auth_service):
#
#     user_id = message.from_user.id
#     code = message.text.strip()
#     auto_logger.info(f'Processing code: {message.from_user.id}')
#     data = await state.get_data()
#     # validation code func
#
#     if await auth_service.verify_code_http(user_id, code, data.get("email")):
#         await message.answer("Вы можете создать заявку с помощью команды /create_ticket")
#         await state.clear()
#         del_starter(message.from_user.id)
#     else:
#         count = data.get("count")
#         await message.answer(f"Неверный код подтверждения. (Попыток осталось: {count - 1})")
#         await state.update_data(count=count-1)
#         await state.set_state(AuthStates.email)
@router.message(AuthStates.code_)
async def process_code(message: types.Message, state: FSMContext, auth_service: AuthService = F.auth_service):
    user_id = message.from_user.id
    code = message.text.strip()

    auto_logger.info(f'Processing code for {user_id}')
    data = await state.get_data()
    email = data.get("email")
    count = data.get("count", 5)

    if await auth_service.verify_code_http(user_id, code, email):
        await message.answer("Вы успешно авторизованы! Используйте /create_ticket для создания заявки.")
        await state.clear()
        del_starter(user_id)
    else:
        count -= 1
        await state.update_data(count=count)
        await message.answer(f"Неверный код. Попыток осталось: {count}")
        if count > 0:
            await state.set_state(AuthStates.email)
        else:
            await add_blacklist(user_id)
            auto_logger.info(f'User blacklisted after failed attempts: {user_id}')
            await state.clear()


def register_start_handlers(dp: Dispatcher, auth_service):
    dp.include_router(router)
    dp['auth_service'] = auth_service
