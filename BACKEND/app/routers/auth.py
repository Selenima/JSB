from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr

from utils.database import get_db, AsyncSession
from services.auth_service import AuthService
from repositories import redis_repository, user_repository
from repositories.redis_repository import RedisRepository
from schemas.auth_response import OTPData, EmailResponse
from models.superset import AuthServiceSuperset
from utils import auto_logger

router = APIRouter(prefix="/auth", tags=["auth"])


class EmailRequest(BaseModel):
    email: EmailStr
    tg_user_id: int

class OTPRequest(BaseModel):
    tg_user_id: int
    code: str
    email: str



@router.post('/send-code', status_code=status.HTTP_201_CREATED)
async def send_code(request: EmailRequest, superset: AuthServiceSuperset = Depends(AuthServiceSuperset), session: AsyncSession = Depends(get_db)):
    """
    Отправка кода подтверждения.
    """
    auto_logger.info(f'{request.model_dump()}')
    service = AuthService(superset.redis_repository, user_repository, session)
    code = await service.send_otp(str(request.email), request.tg_user_id)

    if not code:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Could not send OTP')

    response = EmailResponse(status='success', data=OTPData(email=request.email))
    return response

@router.post('/verify-code', status_code=status.HTTP_201_CREATED)
async def verify_code(request: OTPRequest, session: AsyncSession = Depends(get_db)):
    """
    Проверка кода подтверждения.
    """
    auto_logger.info(f'{request.model_dump()}')

    auto_logger.debug(f"Verifying code: {request.model_dump()}")

    auth_service = AuthService(redis_repository, user_repository, session)


    is_valid = await auth_service.redis_rep.verify_otp(request.tg_user_id, str(request.email), request.code)

    auto_logger.debug(f"Code processed: {is_valid}")

    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid code')



    exec_stat = await auth_service.add_user(str(request.email), request.tg_user_id)
    auto_logger.debug(f'Code exit: {exec_stat}')
    if not exec_stat:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Cannot add user')

    session_key = await redis_repository.create_session(request.tg_user_id, str(request.email)) ####
    return {'status': 'success', 'data': dict(session_key=session_key)}
