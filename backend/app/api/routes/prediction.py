from fastapi import APIRouter, Depends, HTTPException, status,Query
from app.schemas.prediction import HouseInput, PredictionResponse, ResultCountBySuburb, ResultAveragePriceBySuburb,ResultForAllPrediction
from app.service.model_loader import load_model, precess_data, return_sample_input
from app.core.exceptions import CustomHTTPException
from app.core.security import role_required
from app.core.database import get_db
from app.core.exceptions import CustomHTTPException
from app.schemas.prediction import PredictionSaveRequest
from app.service.prediction_service import PredictionService
from app.schemas.response import ResponseSchema
from datetime import date
from typing import List, Optional
from app.constants import Constants


from app.schemas.auth import TokenData
import numpy as np
import pandas as pd

router = APIRouter()

model = load_model() 

X_columns = precess_data()

def preprocess_input(input_data):
    # Convert the input data into a DataFrame
    input_df = pd.DataFrame([input_data.dict()])

    # Convert 'Date' to 'Year'
    input_df['Year'] = pd.to_datetime(input_df['Date']).dt.year
    input_df.drop(columns=['Date'], inplace=True)

    # One-hot encode categorical variables
    input_df = pd.get_dummies(input_df, columns=['Suburb', 'Postcode'], drop_first=True)

    # Ensure all columns match the model input
    input_df = input_df.reindex(columns=X_columns, fill_value=0)
    
    return input_df


@router.post("/predict", response_model=ResponseSchema[PredictionResponse])
async def predict_price(request: HouseInput, current_user: TokenData = Depends(role_required([])),
            db=Depends(get_db)):
    try:
        input_df = preprocess_input(request);

        # Make prediction
        predicted_price = model.predict(input_df) 

        # Save prediction
        prediction = PredictionSaveRequest(
            suburb = request.Suburb,
            rooms = request.Rooms,
            date = request.Date,
            postcode = request.Postcode,
            distance = request.Distance,
            price = predicted_price,
            userId = current_user.userId
        )
        PredictionService.save_prediction(db, prediction)

        # Return prediction
        return ResponseSchema(
                isSuccessful=True,
                statusCode=status.HTTP_201_CREATED,
                message="Prediction created successfully",
                data= PredictionResponse(predicted_price=predicted_price)
            )
    except Exception as e:
        raise CustomHTTPException(status_code=500, message=str(e))


# Search result by seberbs
@router.get("/resultBySuburbs", response_model=ResponseSchema[list[ResultCountBySuburb]])
def predict_result_by_Suburbs(current_user: TokenData = Depends(role_required([Constants.USER.ROLES.ADMIN])), date: Optional[date] = Query(None), db=Depends(get_db)):
    try:
        result = PredictionService.get_result_by_suburbs(date, db)
        return ResponseSchema(
                isSuccessful=True,
                statusCode=status.HTTP_200_OK,
                message="",
                data= result
            )

    except Exception as e:
        raise CustomHTTPException(status_code=500, message=str(e))
    

@router.get("/yearlySuburbsPrice/{suburb}", response_model=ResponseSchema[list[ResultAveragePriceBySuburb]])
def predict_result_by_Suburbs(suburb: str,current_user: TokenData = Depends(role_required([Constants.USER.ROLES.ADMIN])), db=Depends(get_db)):
    try:
        result = PredictionService.get_result_by_suburbs_by_year(suburb, db)
        return ResponseSchema(
                isSuccessful=True,
                statusCode=status.HTTP_200_OK,
                message="",
                data= result
            )

    except Exception as e:
        raise CustomHTTPException(status_code=500, message=str(e))
    
@router.get("/allPredictionForMonth", response_model=ResponseSchema[list[ResultForAllPrediction]])
def predict_result_by_Suburbs(
    current_user: TokenData = Depends(role_required([Constants.USER.ROLES.ADMIN])),
    date: Optional[date] = Query(None),db=Depends(get_db)):
    try:
        result = PredictionService.get_prediction_by_month(date, db)
        return ResponseSchema(
                isSuccessful=True,
                statusCode=status.HTTP_200_OK,
                message="",
                data= result
            )

    except Exception as e:
        raise CustomHTTPException(status_code=500, message=str(e))

@router.get("/getAllStubData", response_model=ResponseSchema[Optional[List[dict]]])
def get_all_stub_data(current_user: TokenData = Depends(role_required([]))):
    try:
        result = return_sample_input()
        return ResponseSchema(
                isSuccessful=True,
                statusCode=status.HTTP_200_OK,
                message="",
                data= result
            )

    except Exception as e:
        raise CustomHTTPException(status_code=500, message=str(e))
    

@router.get("/getAllPredictionData", response_model=ResponseSchema[Optional[List[dict]]])
def get_all_prediction_data(current_user: TokenData = Depends(role_required([]))):
    try:
        result = PredictionService.return_prediction_input(current_user.userId)
        return ResponseSchema(
                isSuccessful=True,
                statusCode=status.HTTP_200_OK,
                message="",
                data= result
            )

    except Exception as e:
        raise CustomHTTPException(status_code=500, message=str(e))
    
@router.get("/getAllPredictionDataByUser", response_model=ResponseSchema[Optional[List[dict]]])
def get_all_prediction_data_by_user(current_user: TokenData = Depends(role_required([])), db=Depends(get_db)):
    try:
        result = PredictionService.return_prediction_input_by_user(current_user.userId, db)
        return ResponseSchema(
                isSuccessful=True,
                statusCode=status.HTTP_200_OK,
                message="",
                data= result
            )

    except Exception as e:
        raise CustomHTTPException(status_code=500, message=str(e))
    