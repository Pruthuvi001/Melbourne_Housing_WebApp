from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import UserLoginRequest,UserLoginResponse
from app.core.database import get_db
from app.core.exceptions import CustomHTTPException
from app.schemas.response import ResponseSchema
from app.service.auth_service import AuthService

router = APIRouter()

@router.post("/login", response_model=ResponseSchema[UserLoginResponse])
def login(request: UserLoginRequest, db=Depends(get_db)):
    try:
        user = AuthService.authenticate_user(db, request)
        return ResponseSchema(
            isSuccessful=True,
            statusCode=status.HTTP_200_OK,
            message="User logged in successfully",
            data=user
        )
    except CustomHTTPException as e:
        raise e
    except Exception as e:
        raise CustomHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )