from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.database import get_session
from app.authentication import utils, oauth2
from app.db.schemas import Token
from sqlmodel import select
from app.db.models import User

router = APIRouter(prefix= '/login', tags= ['Authetication'])

@router.post('/', response_model=Token, status_code=status.HTTP_200_OK)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
                db: AsyncSession= Depends(get_session)):

    statement = select(User).where(User.email == user_credentials.username)
    user_db = await db.exec(statement)
    user = user_db.first()

    if user and utils.verify_password(user_credentials.password, user.password):

        access_token =  oauth2.create_access_token({"id" : str(user.id)})

        return {"access_token": access_token, "token_type": "bearer"} 

    else:
            raise HTTPException (status_code=status.HTTP_403_FORBIDDEN,
                                 detail= "Invalide user credentials")


    



