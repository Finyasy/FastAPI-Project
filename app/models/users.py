from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import func
from sqlalchemy.orm import relationship
from db.config import Base

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    tasks = relationship('TaskModel', back_populates='Owner')
    