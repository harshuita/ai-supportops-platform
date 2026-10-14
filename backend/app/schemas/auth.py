from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: str = "support_agent"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str