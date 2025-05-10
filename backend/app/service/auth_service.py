from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import UserLoginRequest, UserLoginResponse
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import CustomHTTPException

class AuthService:
    @staticmethod
    def authenticate_user(db: Session, request : UserLoginRequest) -> UserLoginResponse:
        # Get user from database
        user = db.query(User).filter_by(email=request.email).first()
        if not user:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Email or password is incorrect!",
            )

        # Verify password
        if not verify_password(request.password, user.password):
            raise CustomHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Email or password is incorrect!",
            )
        
        # Generate token
        data = {
            "userId": user.userId,
            "role": user.role
        }
        token = f"Bearer {create_access_token(data=data)}"
        
        return UserLoginResponse(
            userId=user.userId,
            name=user.name,
            email=user.email,
            mobileNumber=user.mobileNumber,
            role=user.role,
            token=token,
        )