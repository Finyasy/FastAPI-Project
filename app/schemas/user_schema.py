from pydantic import BaseModel
from typing import List,Any,Optional
from schemas.task_schema import TaskOut
from datetime import datetime

class UserBase(BaseModel):
    username:str
    email:str

class UserCreate(UserBase):
    password:str

class UserOut(UserBase):
    id:int
    active:bool
    created_on:Optional[datetime]
    tasks:List[TaskOut]=[]

    class Config:
        orm_mode = True

