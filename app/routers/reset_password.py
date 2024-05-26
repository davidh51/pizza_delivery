from fastapi import APIRouter, HTTPException, status, Depends, Response
from app.db.schemas import PasswordReset, NewPasssword, UserResponse, TokenData
from app.authentication.oauth2 import create_access_token, get_current_user
from app.mail.send_mail import password_reset
from app.authentication.utils import hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db.models import User
from app.db.database import get_session
from uuid import UUID


router = APIRouter(tags=["Reset Password"])

@router.post('/request',status_code=status.HTTP_200_OK, response_description='Request for reset')
async def reset_request(user_email: PasswordReset, db: AsyncSession= Depends(get_session),
                        current_user: AsyncSession= Depends(get_current_user)):

    statement = select(User).where(User.email == user_email.email)
    user_db = await db.exec(statement)
    user = user_db.first()

    if user and current_user == user.id:
        
        token = create_access_token({"id" : str(user.id)})
        reset_link = f"http://localhost:8000/?token={token}"
        #reset_link = f"http://localhost:8000/docs#/Reset%20Password/reset_reset__token__put"

        await password_reset("Password Reset", user.email, 
                             {"title" : "Password Reset",
                             "id" : user.id,
                             "reset_link" : reset_link})
        return({"Email":"sent"})
        
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid credentials")
    
    
@router.put("/reset", response_model=UserResponse,status_code=status.HTTP_200_OK)
async def reset(token: str, new_password: NewPasssword, db: AsyncSession = Depends(get_session)):

    user_id:str = await get_current_user(token, db)

    try:
        statement = select(User).where(User.id == user_id)
        user_db = await db.exec(statement)
        user= user_db.first()

        user.password = hash(new_password.password)
        
        await db.commit()
        return user

    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= "User info not found")
    


    



