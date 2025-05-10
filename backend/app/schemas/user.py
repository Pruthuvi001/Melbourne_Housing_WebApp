from pydantic import BaseModel, EmailStr  
from typing import Optional, Any
class CreateUser(BaseModel):
    name: str
    email: EmailStr
    mobileNumber: str
    role: int
    password: str

class UpdateUser(BaseModel):
    name: str
    email: EmailStr
    mobileNumber: str
    role: int

class UserResponse(BaseModel):
    userId: int = 0
    name: Any  
    email: Any  
    mobileNumber: Any  
    role: Any  
    status: Any
    createdAt: Any
    updatedAt: Any

    class Config:
        from_attributes = True
