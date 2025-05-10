from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar('T')

class ResponseSchema(BaseModel, Generic[T]):
    isSuccessful: bool
    statusCode: int
    message: str
    data: Optional[T] = None


