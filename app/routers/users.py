from fastapi import APIRouter, status, Depends
from app.db.schemas import UserResponse, UserCreate
from app.db.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.routers.users_service import UserService
from app.mail.send_mail import send_registration_mail

router = APIRouter (prefix='/users', tags=['Users'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user_info: UserCreate, db: AsyncSession= Depends(get_session)):

     new_user = await UserService(db).create_user(user_info)

     await send_registration_mail("Registration succesfull", new_user.email,
                                 {"title" : "Registration succesfull",
                                 "ID" : new_user.id})

     return new_user

@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user_id: str, db: AsyncSession= Depends(get_session)):
     
     user = await UserService(db).get_user(user_id)
     return user
     