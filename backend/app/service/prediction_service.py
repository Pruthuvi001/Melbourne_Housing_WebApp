from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.prediction import PredictionSaveRequest, ResultCountBySuburb, ResultAveragePriceBySuburb,ResultForAllPrediction
from app.models.prediction import Prediction
from app.models.user import User
from app.core.exceptions import CustomHTTPException
from sqlalchemy import func
import pandas as pd
from datetime import date

class PredictionService:
    @staticmethod
    def save_prediction(db: Session, request : PredictionSaveRequest) :
        try:
            year = pd.to_datetime(request.date).year
            prediction = Prediction(
                suburb = request.suburb,
                rooms = request.rooms,
                date = year,
                postcode = request.postcode,
                distance = request.distance,
                price = round(request.price, 2),
                userId = request.userId
            )
            db.add(prediction)
            db.commit()
            db.refresh(prediction)
            return prediction
        except Exception as e:
            raise CustomHTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e)
            )
        
    @staticmethod
    def get_result_by_suburbs(given_date : date, db: Session) :
        if given_date is None:
            given_date = date.today()

        # get first day of the month
        first_day_of_month = given_date.replace(day=1)

        # get last day of the month
        last_day_of_month = given_date.replace(day=1) + pd.offsets.MonthEnd()
        try:
            result = (
                db.query(
                    Prediction.suburb,
                    func.count(Prediction.predictionId).label('prediction_count'),  
                    func.avg(Prediction.distance).label('average_distance'), 
                )
                .filter(
                    Prediction.createdAt >= first_day_of_month,
                    Prediction.createdAt <= last_day_of_month
                )
                .group_by(Prediction.suburb)
                .order_by(func.count(Prediction.predictionId).desc())
                .all()
            ) 

            if len(result) == 0:
                return []

            list_result = [ResultCountBySuburb(suburb=row[0], count=row[1]) for row in result]
            return list_result
        except Exception as e:
            raise CustomHTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e)
            )
    
    @staticmethod
    def get_result_by_suburbs_by_year(suburb : str, db: Session) :
        try:
            # Only for this year
            result = (
                db.query(
                    Prediction.date,
                    func.avg(Prediction.price).label('average_price'), 
                )
                .filter(
                    Prediction.suburb == suburb
                )
                .group_by(Prediction.date)
                .order_by(Prediction.date)
                .all()
            )

            if len(result) == 0:
                return []
            
            list_result = [ResultAveragePriceBySuburb(year=row[0], average_price=row[1]) for row in result]
            return list_result
        except Exception as e:
            raise CustomHTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e)
            )

    @staticmethod
    def get_prediction_by_month(given_date : date, db: Session) :
        try:
            if given_date is None:
                given_date = date.today()

            # get first day of the month
            first_day_of_month = given_date.replace(day=1)

            # get last day of the month
            last_day_of_month = given_date.replace(day=1) + pd.offsets.MonthEnd()

            result = (
                db.query(
                    Prediction.suburb,
                    Prediction.rooms,
                    Prediction.date,
                    Prediction.postcode,
                    Prediction.distance,
                    Prediction.price,
                    User.name,
                    Prediction.createdAt
                )
                .join(User, User.userId == Prediction.userId)
                .filter(
                    Prediction.createdAt >= first_day_of_month,
                    Prediction.createdAt <= last_day_of_month
                )
                .all()
            )

            if len(result) == 0:
                return []
            
            list_result = [ResultForAllPrediction(suburb=row[0], rooms=row[1], date=row[2], postcode=row[3], distance=row[4], price=row[5], userName=row[6], dateTime=row[7]) for row in result]

            return list_result
        except Exception as e:
            raise CustomHTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e)
            )

    @staticmethod
    def return_prediction_input(userId : int, db: Session) :
        try:
            result = (
                db.query(
                    Prediction.suburb,
                    Prediction.rooms,
                    Prediction.date,
                    Prediction.postcode,
                    Prediction.distance,
                    Prediction.price,
                    User.name,
                    Prediction.createdAt
                )
                .join(User, User.userId == Prediction.userId)
                .filter(
                    Prediction.userId == userId
                )               
                .all()
            )

            if len(result) == 0:
                return []
            
            list_result = [ResultForAllPrediction(suburb=row[0], rooms=row[1], date=row[2], postcode=row[3], distance=row[4], price=row[5], userName=row[6], dateTime=row[7]) for row in result]

            return list_result
        except Exception as e:
            raise CustomHTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e)
            )
        

    @staticmethod
    def return_prediction_input_by_user(userId : int, db: Session) :
        current_month = date.today().replace(day=1)

        try:
            result = (
                db.query(
                    Prediction.suburb,
                    Prediction.rooms,
                    Prediction.date,
                    Prediction.postcode,
                    Prediction.distance,
                    Prediction.price,
                    User.name,
                    Prediction.createdAt
                )
                .join(User, User.userId == Prediction.userId)
                .filter(
                    Prediction.userId == userId,
                    Prediction.createdAt >= current_month
                )               
                .all()
            )

            if len(result) == 0:
                return []
            
            list_result = [
            ResultForAllPrediction(
                suburb=row[0],
                rooms=row[1],
                date=row[2],
                postcode=row[3],
                distance=row[4],
                price=row[5],
                userName=row[6],
                dateTime=row[7]
            ).dict()  
            for row in result
        ]


            return list_result
        except Exception as e:
            raise CustomHTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e)
            )