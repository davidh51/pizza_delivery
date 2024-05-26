from jose import JWTError, jwt 
from datetime import datetime, timedelta 
from app.config import settings 
from app.db.schemas import TokenData
from app.db.models import User
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.database import get_session
from sqlmodel import select
from uuid import UUID


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login/')

ALGORITHM = settings.ALGORITHM 
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = settings.SECRET_KEY

def create_access_token (payload: dict):
    to_encode = payload.copy()

    expiration_time =  datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expiration_time})

    jwt_token = jwt.encode (to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return jwt_token

def verify_access_token (token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        id: str= payload.get("id")

        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data

async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: AsyncSession= Depends(get_session)):

    credentials_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Token could not verify credentails", 
                                         headers= {"WWW-Authenticate":"Bearer"})

    current_user_id= verify_access_token(token, credentials_exception).id
    
    statement = select(User).where(User.id == UUID(current_user_id)) 
    user_db = await db.exec(statement)
    current_user = user_db.first()
   
    return current_user.id

