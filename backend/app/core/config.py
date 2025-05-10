from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import ClassVar

# load .env
load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    app_name: str = "HousePricing"
    version: str 
    jwt_secret: str 
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str
    MODEL_PATH: ClassVar[Path] = Path(__file__).parent.parent / "trained_model" / "melbourne_house_price_model.joblib"
    DATASET_PATH: ClassVar[Path] = Path(__file__).parent.parent / "trained_model" / "MELBOURNE_HOUSES_DATASET.csv"

    class Config:
        arbitrary_types_allowed = True 

class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()