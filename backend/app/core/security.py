from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from .exceptions import CustomHTTPException
from app.core.config import settings
from app.schemas.auth import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to verify password with hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash password
def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def get_token_data(token: str) -> TokenData:
    try:
        if token is None:
            raise CustomHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="No token provided",
            )
        
        payload  = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return TokenData(
            userId=payload.get("userId"),
            role=payload.get("role"),
        )
    except JWTError:
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid token",
        )
    
def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    username = get_token_data(token)
    if username is None:
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid authentication credentials"
        )
    return username

def role_required(required_roles: List[int] = []):
    def role_checker(current_user: TokenData = Depends(get_current_user)):
        # If required_roles is empty or None, allow access to all roles
        if required_roles and current_user.role not in required_roles:
            raise CustomHTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="You do not have permission to access this resource",
            )
        return current_user
    return role_checker