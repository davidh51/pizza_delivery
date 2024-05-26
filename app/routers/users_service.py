from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db.models import User
from app.db.schemas import UserCreate
from fastapi import HTTPException, status
from app.authentication.utils import hash
from uuid import UUID

class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session 

    async def create_user(self, user_info: UserCreate):

        statement = select(User).where(User.email == user_info.email)
        user_db = await self.session.exec(statement)

        if user_db.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'User: {user_info.email} already exists')
        
        hashed_paswword = hash(user_info.password)
        user_info.password = hashed_paswword

        new_user = User(**user_info.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
    

    async def get_user(self, user_id: str):

        try: 
            statement = select(User).where(User.id == user_id)
            user_db = await self.session.exec(statement)
            user = user_db.first()
        except:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f'Invalid id: {user_id}')

        if not user_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'User with the id: {user_id} does not exists')
        
        return user
