from pydantic import BaseModel, EmailStr  
from typing import Optional, Any
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    userId: int = 0
    name: Any
    email: Any
    mobileNumber: Any
    role: Any
    token: str

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    userId : Optional[int] = None
    role : Optional[int] = None

    class Config:
        from_attributes = True
