from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.core.exceptions import CustomHTTPException
from app.core.error_handlers import (
    http_exception_handler,
    sqlalchemy_exception_handler,
    validation_exception_handler
)
import json

app = FastAPI(
    title=settings.app_name,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    swagger_ui_parameters={"deepLinking": False}
)

# Add exception handlers
app.add_exception_handler(CustomHTTPException, http_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.models.user import User
from app.models.prediction import Prediction
Base.metadata.create_all(bind=engine)

# define route to defalut route for / endpoint
@app.get("/")
async def root():
    return {"message": f"House Pricing API {settings.version} is running..!"} 

# Include routers
from app.api.routes.user import router as user_router
from app.api.routes.auth import router as auth_router
from app.api.routes.prediction import router as prediction_router
from app.api.routes.webSocket import router as websocket_router


# call Router
app.include_router(user_router, prefix=f"{settings.API_V1_STR}/user", tags=["user"])
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(prediction_router, prefix=f"{settings.API_V1_STR}/prediction", tags=["prediction"])
app.include_router(websocket_router, prefix=f"", tags=["websocket"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)