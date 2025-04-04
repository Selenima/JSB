import json

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from repositories.user_repository import UserRepository

from schemas.profile import User, Profile
from utils.database import get_db

router = APIRouter(prefix='/user', tags=['user'])

class GetUserProfileRequest(BaseModel):
    tg_user_id: int

@router.get('/from-db')
async def get_user(request: GetUserProfileRequest, user_repository: UserRepository = Depends()):
    """
    Возвращает профиль пользователя из бд
    """
    async with get_db() as session:
        user = await user_repository.get_user(session, request.tg_user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user #!!!!!  .model_dump() (tg_bot/app/services/auth_service.py ::69)

@router.put('/profile-update', status_code=204)
async def profile_update(request: User, user_repository: UserRepository = Depends()):
    """
    Обновляет пользовательский профиль.
    """
    try:
        user = User.model_validate(request.model_dump())
    except:
        raise HTTPException(status_code=401, detail="Bad request")


    async with get_db() as session:
        user = await user_repository.update_user(session, user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")


