from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from .exceptions import CustomHTTPException
from app.schemas.response import ResponseSchema

async def http_exception_handler(request: Request, exc: CustomHTTPException):
    message = exc.message if exc.message else "Something went wrong!"
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseSchema(
            isSuccessful=False,
            statusCode=exc.status_code,
            message=message
        ).dict()
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    message = str(exc) if str(exc) else "Database error occurred"
    return JSONResponse(
        status_code=500,
        content=ResponseSchema(
            isSuccessful=False,
            statusCode=500,
            message=message,
        ).dict()
    )

async def validation_exception_handler(request: Request, exc: Exception):
    # errors: List[ErrorDetail] = []
    error_message = ""
    error = exc.errors()[0]
    
    # Format the error message
    field_name = error['loc'][-1]  
    error_message = f"{field_name} {error['msg']}" 


    
    return JSONResponse(
        status_code=422,
        content=ResponseSchema(
            isSuccessful=False,
            statusCode=422,
            message= error_message,
        ).dict()
    )