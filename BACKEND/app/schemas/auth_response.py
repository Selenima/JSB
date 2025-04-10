from pydantic import BaseModel, EmailStr


class OTPData(BaseModel):
    email: EmailStr
    code: str


class EmailResponse(BaseModel):
    status: str
    data: OTPData




