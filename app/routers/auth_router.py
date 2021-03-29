




from datetime import timedelta,datetime
from pydantic import BaseModel
from sqlalchemy.orm import Session
from user.service import UserService

router=APIRouter()

# setups for JWT
SECRET_KEY = 'SOME-SECRET-KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context=CryptContext(schemes=['bcrypt'])

#setup the security
OAuth2_schema=OAuth2PasswordBearer(tokenUrl='token')

# token
class Token(BaseModel):
    access_token: str
    token_type: str

@router.post('/register',
summary='register a new user',
status_code=201)
async def register_user(user:UserCreate,db:Session= Depends(get_db)):
    return UserService.create_user(payload=user,db=db)

@router_post('/token',
summary='register a new user',
status_code=201)

#verify user || returns either true or false
def check_password_hash(password,hashed_password):
    return pwd_context.verify(password,hashed_password)












@router.put('/{user_id}',
summary='edits a user that matches the id provided',
response_model= UserOut, 
response_description = 'the user',
status_code = 200)
async def update_user(user_id:int, user:UserCreate,db: Session=Depends(get_db)):
    pass





































#  get active user  
async def get_current_active_user(current_user: UserOut =  Depends(get_current_user)):     
    if not current_user.active:         
        raise HTTPException(status_code=400, detail='User account is deactivated')   
      return current_user  