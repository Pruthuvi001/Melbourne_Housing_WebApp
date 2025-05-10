from pydantic import BaseModel
from typing import Optional, Any

class HouseInput(BaseModel):
    Suburb: str
    Rooms: int
    Date: str
    Postcode: int
    Distance: float

    class Config:
        from_attributes = True

class PredictionResponse(BaseModel):
    predicted_price: float

    class Config:
        from_attributes = True

class PredictionSaveRequest(BaseModel):
    suburb: str
    rooms: int
    date: str
    postcode: int
    distance: float
    price: float
    userId: int

    class Config:
        from_attributes = True

class ResultCountBySuburb(BaseModel):
    suburb: str
    count: int

class ResultAveragePriceBySuburb(BaseModel):
    year: int
    average_price: float

class ResultForAllPrediction(BaseModel):
    suburb: Any
    rooms: Any
    date: Any
    postcode: Any
    distance: Any
    price: Any
    userName: Any
    dateTime: Any