"""
Пакет для работы с хранилищами данных, выполнения CRUD-операций.
Все операции данного типа должны выполняться в рамках репозиториев.
Любые отклонения должны устраняться при рефакторинге.
"""

from cfg import cfg

from .redis_repository import RedisRepository


redis_repository = RedisRepository(cfg) # include

