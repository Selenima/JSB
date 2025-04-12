from aiogram import Dispatcher

from middlewares.auth_middleware import AuthMiddleware
from .start import router as start_router
from .create_ticket import router as create_ticket_router
# from .main_menu import register_main_menu_handlers
# from .profile import register_profile_handlers



def register_handlers(dp: Dispatcher, auth_service, redis_repository, ticket_service):
    dp['auth_service'] = auth_service
    dp['redis_repository'] = redis_repository
    dp['ticket_service'] = ticket_service

    routers = [start_router, create_ticket_router]

    for router in routers:
        router.message.middleware(AuthMiddleware())
        router.callback_query.middleware(AuthMiddleware())

    dp.include_routers(*routers)
