

class DuplicateUserError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class TicketServiceError(Exception):
    """Базовое исключение для сервиса тикетов"""
    pass

class TicketCreationError(TicketServiceError):
    """Ошибка создания тикета"""
    pass

class TicketNotFoundError(TicketServiceError):
    """Тикет не найден"""
    pass