from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from schemas.task_schema import TaskOut

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    active: bool
    created_on: Optional[datetime]
    tasks: List[TaskOut] = []

    class Config:
        orm_mode = True
