from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import CreateUser, UserResponse, UpdateUser
from app.core.database import get_db
from app.core.security import get_current_user, role_required
from app.core.exceptions import CustomHTTPException
from app.schemas.response import ResponseSchema
from app.service.user_service import UserService
from app.schemas.auth import TokenData
from app.constants import Constants
router = APIRouter()

@router.post("/register", response_model=ResponseSchema[UserResponse])
def register_user(user: CreateUser, db=Depends(get_db)):
    try:
        db_user = UserService.create_user(db, user)
        return ResponseSchema(
            isSuccessful=True,
            statusCode=status.HTTP_201_CREATED,
            message="User registered successfully!",
            data=db_user
        )
    except CustomHTTPException as e:
        raise e
    except Exception as e:
        raise CustomHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )
    # return user;

@router.put("/update", response_model=ResponseSchema[UserResponse])
def update_user(user: UpdateUser,current_user: TokenData = Depends(role_required([])), db=Depends(get_db)):
    try:
        db_user = UserService.update_user(db, current_user.userId, user)
        return ResponseSchema(
            isSuccessful=True,
            statusCode=status.HTTP_200_OK,
            message="User updated successfully!",
            data=db_user
        )
    except CustomHTTPException as e:
        raise e
    except Exception as e:
        raise CustomHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )

@router.get("/getById/{user_id}", response_model=ResponseSchema[UserResponse])
def get_user(user_id: int,
            current_user: TokenData = Depends(role_required([])),
            db=Depends(get_db)):
    try:
        db_user = UserService.get_user(db, user_id)

        return ResponseSchema(
            isSuccessful=True,
            statusCode=status.HTTP_200_OK,
            message="",
            data=db_user
        )
    except CustomHTTPException as e:
        raise e
    except Exception as e:
        raise CustomHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )
    
@router.get("/profile", response_model=ResponseSchema[UserResponse])
def get_profile(
    current_user: TokenData = Depends(role_required([])),
    db=Depends(get_db)
):
    try:
        db_user = UserService.get_user(db, current_user.userId)

        return ResponseSchema(
            isSuccessful=True,
            statusCode=status.HTTP_200_OK,
            message="",
            data=db_user
        )
    except CustomHTTPException as e:
        raise e
    except Exception as e:
        raise CustomHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )

@router.get("/getAll", response_model=ResponseSchema[list[UserResponse]])
def get_profile(
    current_user: TokenData = Depends(role_required([Constants.USER.ROLES.ADMIN])),
    db=Depends(get_db)
):
    try:
        db_user = UserService.get_all_users(db)

        return ResponseSchema(
            isSuccessful=True,
            statusCode=status.HTTP_200_OK,
            message="",
            data=db_user
        )
    except CustomHTTPException as e:
        raise e
    except Exception as e:
        raise CustomHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )
