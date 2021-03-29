from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.users import UserModel
from schemas.user_schema import UserCreate
from passlib.context import CryptContext 

pwd_context = CryptContext(schemes=['bcrypt'])

class Userservice:

    @staticmethod
    def fetch_users(db:Session):
        """return a list of all users"""
        return db.query(UserModel).all()

    @staticmethod
    def find_user(user_id:int,db:Session):
        
        """returns a user that matches the id"""
        user=db.query(UserModel).filter(UserModel.id==user_id).first()

        if not user:
            raise HTTPException

        
        return user

    @staticmethod
    def insert_user(payload:UserCreate,db: Session):
        """returns a new user"""
        user = db.query(UserModel).filter(UserModel.email==payload.email).first()

        if user:
            raise HTTPException(status_code=400,detail="User already exists!")

        else:
            record = UserModel(username=payload.username, email=payload.email, password=pwd_context.hash(payload.password))
            db.add(record)
            db.commit()
            db.refresh(record)
            return record

            ###TO DO FOR EDIT AND DELETE##    
    @staticmethod
    def delete_user(user_id:int, db:Session):
        pass