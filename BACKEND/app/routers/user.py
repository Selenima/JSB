import json

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from repositories import redis_repository

from sqlalchemy.ext.asyncio import AsyncSession
from schemas.profile import User, Profile
from utils.database import get_uow, UnitOfWork
from utils import set_logger_filename
from repositories.user_repository import UserRepository

router = APIRouter(prefix='/users', tags=['users'])

# class GetUserProfileRequest(BaseModel):
#     tg_user_id: str

class GetUserProfileResponse(BaseModel):
    status: str
    data: User

@router.get('/from-db')
async def get_user(tg_user_id: str, uow: UnitOfWork = Depends(get_uow)):
    """
    Возвращает профиль пользователя из бд
    """
    logger = set_logger_filename('USER_GETTING')

    logger.info(f'Get user request: {tg_user_id}') # !!!!!!!!!!!!!!!!!!!!!!!


    user = await uow.user_repository.get_user(int(tg_user_id))
    user = User.model_validate(user.__dict__) if user is not None else user
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # session = await redis_repository.get_session(int(tg_user_id))
    # if not session:
    #     return GetUserProfileResponse(status='success', data=user)

    return GetUserProfileResponse(status='success', data=user)

@router.put('/profile-update', status_code=204) #WT
async def profile_update(request: User, uow: UnitOfWork = Depends(get_uow)):
    """
    Обновляет пользовательский профиль.
    """
    try:
        user = User.model_validate(request.model_dump())
    except Exception as e:
        #logger.error(f'HTTP | PUT :{e}')
        raise HTTPException(status_code=401, detail="Bad request")



    user = await uow.user_repository.update_user(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")


