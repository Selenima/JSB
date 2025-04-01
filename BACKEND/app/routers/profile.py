import json

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from repositories.user_repository import UserRepository

from schemas.profile import User, Profile
from utils.database import get_db

router = APIRouter(prefix='/profile', tags=['profile'])

class GetUserProfileRequest(BaseModel):

    tg_user_id: int

@router.get('/')
async def get_user_profile(request: GetUserProfileRequest, user_repository: UserRepository = Depends()):
    """
    Возвращает профиль пользователя из бд
    """
    async with get_db() as session:
        user = await user_repository.get_user_by_tg_id(session, request.tg_user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        p = Profile(full_name=user.full_name, company=user.company, position=user.position, contacts=json.loads(user.contacts))
        user = User(tg_user_id=user.tg_user_id, email=user.email, profile=p)

        return user #!!!!!  .model_dump() (tg_bot/app/services/auth_service.py ::69)

