from .start import register_start_handlers
# from .profile import register_profile_handlers
# from .create_ticket import register_create_ticket_handlers
# from .main_menu import register_main_menu_handlers

def register_handlers(dp, auth_service):
    register_start_handlers(dp, auth_service)#?, auth_service
    # register_profile_handlers(dp)
    # register_create_ticket_handlers(dp)
    # register_main_menu_handlers(dp)
