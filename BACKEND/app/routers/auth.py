from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr

from services.auth_service import AuthService
from services.session_service import SessionService
from repositories.redis_repository import RedisRepository

router = APIRouter(prefix="/auth", tags=["auth"])



class SmtpAgent:

    sender = 'app@mrtexpert.ru'

class EmailRequest(BaseModel):
    email: EmailStr
    tg_user_id: int

class OTPRequest(BaseModel):
    tg_user_id: int
    code_: str
    email: EmailStr

@router.post('/send-code')
async def send_code(request: EmailRequest, redis_rep: RedisRepository = Depends()):
    """
    Отправка кода подтверждения.
    """
    service = AuthService(redis_rep, smtp_sender=SmtpAgent.sender)

    return await service.send_otp(request.email, request.tg_user_id) ####

@router.post('/verify-code')
async def verify_code(request: OTPRequest, redis_rep: RedisRepository = Depends()):
    """
    Проверка кода подтверждения.
    """
    auth_service = AuthService(redis_rep, smtp_sender=SmtpAgent.sender)
    session_service = SessionService(redis_rep)

    is_valid = await auth_service.redis_rep.verify_otp(request.tg_user_id, request.code_)

    if not is_valid:
        return HTTPException(status_code=400, detail='Invalid code')


    exec_stat = await auth_service.add_user(request.email, request.tg_user_id)
    if not exec_stat:
        return HTTPException(status_code=401, detail='Cannot add user')

    session_key = await session_service.create_session(request.tg_user_id, request.email) ####
    return {'session_key': session_key}
