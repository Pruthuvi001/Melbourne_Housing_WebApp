from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Double
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship
from app.constants import Constants

class Prediction(Base):
    __tablename__ = "Prediction"

    predictionId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    suburb = Column(String(255), nullable=False) 
    rooms = Column(Integer, nullable=False) 
    date = Column(Integer, nullable=False) 
    postcode = Column(Integer, nullable=False)
    distance = Column(Double, nullable=False)
    price = Column(Double, nullable=False)
    userId = Column(Integer, ForeignKey("User.userId"), nullable=False)
    status = Column(Integer, nullable=False, default=Constants.STATUS.ACTIVE)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

    user = relationship("User", back_populates="predictions")


