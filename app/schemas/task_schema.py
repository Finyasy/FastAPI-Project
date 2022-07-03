from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    note: str
    user_id: int

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    completed: bool
    created_on: str

    class Config:
        orm_mode = True
