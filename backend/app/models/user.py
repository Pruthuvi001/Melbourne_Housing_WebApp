from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
from app.constants import Constants
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "User"

    userId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False) 
    email = Column(String(255), nullable=False, unique=True) 
    mobileNumber = Column(String(20), nullable=False) 
    role = Column(Integer, nullable=False)
    password = Column(String(255), nullable=False) 
    status = Column(Integer, nullable=False, default=Constants.STATUS.ACTIVE)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

    predictions = relationship("Prediction", back_populates="user")
