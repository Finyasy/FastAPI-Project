from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from jose import JWTError,jwt
from typing import Optional, Any
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from pydantic import BaseModel


# database setup
from db.config import Base, engine, get_db
from models.users import UserModel
from models.tasks import TaskModel
Base.metadata.create_all(bind=engine)


# routers 
from routers import task_router, user_router




# token
class Token(BaseModel):
    access_token: str
    token_type: str




# setups for JWT
SECRET_KEY = 'SOME-SECRET-KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30




# setup passlib object to manage your hashes and related policy configuration.
pwd_context = CryptContext(schemes=['bcrypt'])


"""
    Replace this list with the hash(es) you wish to support.
    this example sets pbkdf2_sha256 as the default,
    with additional support for reading legacy des_crypt hashes.


"""


# setup the security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




app = FastAPI(
    title="Implementing Security",
    description="Project to implement security in FastAPI",
    version="1.0.0"
)




# verify user || returns either true or false
def check_password_hash(password, hashed_passed):
    return pwd_context.verify(password, hashed_passed)


# authenticate user
def authenticate_user(db:Session,username:str, password:str):
    user = db.query(UserModel).filter(UserModel.username==username).first()
    if not user:
        return False
    if not check_password_hash(password=password, hashed_passed=user.password):
        return False
    return user




# create access token
def create_access_token(identity:dict, expires_delta:Optional[timedelta] = None):
    """setup expiry for your tokens"""
    new_identity = identity.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        """default expiry time will be 15minutes"""
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    # update your your dict
    new_identity.update({'exp':expire})
    # encoded toke
    encoded_jwt = jwt.encode(claims=new_identity, key=SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


# get current user
async def get_identity(token: str = Depends(oauth2_scheme)):
    exception = HTTPException(
        status_code=401,
        detail='invalid credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )
  
    try:
        # decode the token
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        identity:str  = payload.get('sub')
        if identity is None:
            raise exception
    except JWTError:
        raise exception


    return identity




@app.get('/')
async def home():
    return {"message":"Welcome"}


@app.post('/token', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(identity={'sub': user.id}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}
    


app.include_router(
    user_router.router,
    prefix='/users',
    tags=['User Operations'],
    responses={200:{'description':'Ok'}, 201:{'description':'Created'}, 400:{'description':'Bad Request'}, 401:{'desription':'Unauthorized'}}
)


app.include_router(
    task_router.router,
    prefix='/tasks',
    tags=['Task Operations'],
    dependencies=[Depends(get_identity)],
    responses={200:{'description':'Ok'}, 201:{'description':'Created'}, 400:{'description':'Bad Request'}, 401:{'desription':'Unauthorized'}}
)