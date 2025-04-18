from pydantic import BaseModel, EmailStr


class OTPData(BaseModel):
    email: EmailStr
    code: str


class EmailResponse(BaseModel):
    status: str
    data: OTPData # на данном этапе гипертрофированный ответ, но не хочу урезать возможно оправдается позже
