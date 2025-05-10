from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

DATABASE_URL = "mssql+pyodbc://sa:1234@PRUTHUVI-PC\SQLEXPRESS/HousePricing?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=no"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
