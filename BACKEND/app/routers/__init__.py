from fastapi import FastAPI
from . import auth, tickets, user

__all__ = ['auth', 'user', 'tickets', 'include_routers']

def include_routers(app: FastAPI, prefix: str = None):
    """Подключаем все роутеры"""

    app.include_router(auth.router, prefix=prefix if prefix else None)
    app.include_router(tickets.router, prefix=prefix if prefix else None)
    app.include_router(user.router, prefix=prefix if prefix else None)