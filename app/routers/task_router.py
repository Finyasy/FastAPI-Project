from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List

#db imports
from db.config import get_db
from schemas.task_schema import TaskCreate,TaskOut

router = APIRouter()

# service
from services.task_services import TaskService

@router.get('',
summary='return a list of tasks',
response_model=List[TaskOut],
response_description= 'all tasks',
status_code = 200
)
async def get_all_tasks(db:Session = Depends(get_db)):
    return TaskService.fetch_tasks(db=db)

@router.get('/{task_id}',
summary='return a task that matches the id',
response_model=TaskOut,
response_description='the task',
status_code=200
)
async def get_task(task_id:int,db: Session = Depends(get_db)):
    return TaskService.find_task(task_id=task_id, db=db)

@router.post('',
summary='create a new task',
response_model=TaskOut,
response_description='the new task',
status_code=201
)
async def create_task(task:TaskCreate,db:Session = Depends(get_db)):
    pass

@router.delete('/{task_id}',
summary='deletes a task that matches the id',
response_model=TaskOut,
response_description='the task',
status_code=201
)
async def delete_task(task_id:int,db: Session=Depends(get_db)):
    pass