"""
Пакет для работы с хранилищами данных, выполнения CRUD-операций.
Все операции данного типа должны выполняться в рамках репозиториев.
Любые отклонения должны устраняться при рефакторинге.
"""

from cfg import cfg

from .redis_repository import RedisRepository
from .user_repository import UserRepository
from .ticket_repository import TicketRepository

__all__ = ['RedisRepository', 'UserRepository', 'TicketRepository']
