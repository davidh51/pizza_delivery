from fastapi import  HTTPException, status, Depends, APIRouter
from app.db.models import  Vote
from app.db.schemas import VoteModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.authentication.oauth2 import get_current_user
from app.db.database import get_session
from sqlmodel import select 
from uuid import UUID


router = APIRouter(prefix='/votes', tags=['Vote'])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: VoteModel, db:AsyncSession = Depends(get_session), 
               current_user: str= Depends(get_current_user)):
    
        statement = select(Vote).where(Vote.book_id == vote.book_id,
                                       Vote.user_id == current_user)
        vote_db = await db.exec(statement)
        vote_found = vote_db.first()
       
        if (vote.dir == 1):#dir 0 es para borrar, dir 1 para dar like
            if vote_found:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=
                    f'El User {current_user} has already voted on book {vote.book_id}')
            
            
            new_vote = Vote(book_id = vote.book_id, user_id = current_user)
            db.add(new_vote)
            await db.commit()
            return {"Message":"Succesfully added vote"}
        
        else:
            if not vote_found:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
                          f"Book {vote.book_id} does not exit")
            
            await db.delete(vote_found)
            await db.commit()
            return {"Message":"Succesfully deleted"}


        
       
    
        
           
    
        

            

    
 
