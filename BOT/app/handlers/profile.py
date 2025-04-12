# from aiogram import types, Router, Dispatcher
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.filters import Command
#
# from app.keyboards.profile import get_profile_keyboard
#
# router = Router()
#
# class ProfileStates(StatesGroup):
#     editing = State()
#
# @router.message(Command('profile'))
# async def show_profile(message: types.Message):
#
#     user = await user_repository.get_user(message.from_user.id)
#     await message.answer(
#         f'Current user:\n'
#         f'Full name: {user.full_name}\n'
#         f'Company: {user.company}\n'
#         f'Position: {user.position}\n'
#         f'Phone: {user.phone_number}\n',
#         reply_markup = get_profile_keyboard()
#     )
#
# @router.message(ProfileStates.editing)
# async def edit_profile(message: types.Message, state: FSMContext):
#
#     # Base profile editing
#
#     await message.answer('Profile edited!')
#     await state.clear()
#
# def register_profile_handlers(dp: Dispatcher):
#     dp.include_router(router)