import dataclasses

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr

from services.auth_service import AuthService
from repositories.redis_repository import RedisRepository
from schemas.auth_response import OTPData, EmailResponse

router = APIRouter(prefix="/auth", tags=["auth"])


class EmailRequest(BaseModel):
    email: EmailStr
    tg_user_id: int

class OTPRequest(BaseModel):
    tg_user_id: int
    code_: str
    email: EmailStr



@router.post('/send-code', status_code=status.HTTP_200_OK)
async def send_code(request: EmailRequest, redis_rep: RedisRepository = Depends()):
    """
    Отправка кода подтверждения.
    """
    service = AuthService(redis_rep)
    code = await service.send_otp(str(request.email), request.tg_user_id)

    if not code:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Could not send OTP')

    response = EmailResponse(status='success', data=OTPData(email=request.email, code=code))
    return response

@router.post('/verify-code', status_code=status.HTTP_201_CREATED)
async def verify_code(request: OTPRequest, redis_rep: RedisRepository = Depends()):
    """
    Проверка кода подтверждения.
    """
    auth_service = AuthService(redis_rep)


    is_valid = await auth_service.redis_rep.verify_otp(request.tg_user_id, request.code_)

    if not is_valid:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid code')


    exec_stat = await auth_service.add_user(str(request.email), request.tg_user_id)
    if not exec_stat:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Cannot add user')

    session_key = await redis_rep.create_session(request.tg_user_id, str(request.email)) ####
    return {'status': 200, 'data': dict(session_key=session_key)}
