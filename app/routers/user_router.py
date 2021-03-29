from fastapi import APIRouter, Depends,HTTPException
from typing import List
from sqlalchemy.orm import Session

# db imports
from db.config import get_db

from services.user_services import Userservice

# schemas imports
from schemas.user_schema import UserCreate ,UserOut

router = APIRouter()

@router.get('',
summary='return a list of all users',
response_model= List[UserOut], 
response_description = 'all users',
status_code = 200
)
async def get_all_users(db: Session = Depends(get_db)):
    return Userservice.fetch_users(db=db)

@router.get('/{user_id}',
summary='returns a single user that matches the id provided',
response_model= List[UserOut], 
response_description = 'the user',
status_code = 200
)
async def get_user(user_id:int, db: Session=Depends(get_db)):
    return Userservice.find_user(user_id=user_id, db=db)

@router.post('',
summary='creates a new user',
response_model= UserOut, 
response_description = 'the new user',
status_code = 201)
async def create_user(user: UserCreate,db: Session=Depends(get_db)):
    return Userservice.insert_user(payload=user,db=db )

@router.put('/{user_id}',
summary='edits a user that matches the id provided',
response_model= UserOut, 
response_description = 'the user',
status_code = 200)
async def update_user(user_id:int, user:UserCreate,db: Session=Depends(get_db)):
    pass

@router.delete('/{user_id}',
summary='deletes a user that matches the id provided',
response_model= UserOut, 
response_description = 'the user',
status_code = 200)
async def delete_user(user_id:int,db: Session=Depends(get_db)):
    pass