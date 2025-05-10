from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import CreateUser, UpdateUser
from app.models.user import User
from app.core.security import get_password_hash, verify_password
from app.core.exceptions import CustomHTTPException
from app.constants import Constants

class UserService:
    @staticmethod
    def create_user(db: Session, user: CreateUser) -> User:
        # Validate user email
        UserService.ValidateUserObject(user)
        
        user_exist = db.query(User).filter_by(
            email=user.email,
            status=Constants.STATUS.ACTIVE
        ).first()
        if user_exist:
            raise CustomHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Email already registered",
            )

        # Create user
        try:
            hashed_password = get_password_hash(user.password)
            new_user = User(
                name = user.name,
                email = user.email,
                mobileNumber = user.mobileNumber,
                role = user.role,
                password = hashed_password,
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except Exception as e:
            db.rollback()
            raise CustomHTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Failed to create user",
            )
        
    @staticmethod
    def update_user(db: Session, user_id: int, user: UpdateUser):
        UserService.ValidateUserObject(user, is_update=True)

        # Get existing user from database 
        db_user = db.query(User).filter_by(userId=user_id,status=Constants.STATUS.ACTIVE).first()
        if not db_user:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User not found",
            )

        # Update the user
        try:
            db_user.name = user.name
            db_user.email = user.email
            db_user.mobileNumber = user.mobileNumber
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except Exception as e:
            db.rollback()
            raise CustomHTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Failed to Update user",
            )
      
    @staticmethod
    def get_user(db: Session, user_id: int):
        db_user = db.query(User).filter_by(userId=user_id,status=Constants.STATUS.ACTIVE).first()
        if not db_user:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User not found",
            )
        return db_user
    
    @staticmethod  
    def ValidateUserObject(user: User, is_update: bool = False):
        message = ""
        if not user.name:
            message = "Name is required"
        elif not user.email:
            message = "Email is required"
        elif not user.mobileNumber:
            message = "Mobile Number is required"
        elif not is_update and not user.role:
            message = "Role is required"
        elif not is_update and not user.password:
            message = "Password is required"

        if message:
            raise CustomHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=message,
            )
        
    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).filter_by(status=Constants.STATUS.ACTIVE, role=Constants.USER.ROLES.USER).all()
    