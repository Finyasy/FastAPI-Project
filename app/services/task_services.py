from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.tasks import TaskModel
from schemas.task_schema import TaskCreate, TaskOut


class TaskService:


    @staticmethod
    def fetch_tasks(db:Session):
        """return a list of all tasks"""
        return db.query(TaskModel).all()


    @staticmethod
    def find_task(task_id:int,db:Session):
        """return a task that matches the id"""
        task = db.query(TaskModel).filter(TaskModel.id==task_id).first()
        if task is None:
            raise HTTPException(status_code=404, detail='task does not exist')
        return task