from fastapi import FastAPI
from . import auth, tickets, user

__all__ = ['auth', 'user', 'tickets', 'include_routers']

def include_routers(app: FastAPI):
    """Подключаем все роутеры"""

    app.include_router(auth.router)
    app.include_router(tickets.router)
    app.include_router(user.router)