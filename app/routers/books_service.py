from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db.models import Book, Vote 
from app.db.schemas import BookCreate
from fastapi import HTTPException, status
from sqlalchemy import func

class BookService:
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_books(self):
        
        try:
            #statement = select(Book).order_by(Book.created_at)
            statement = (select(Book, func.count(Vote.book_id).label("vote")).
                        join(Vote,Vote.book_id == Book.id, isouter=True).group_by(Book.id))
 
            result = await self.session.exec(statement)
            return result.all()
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'There is no books')
    
    async def get_one_book(self, book_uid: str, current_user: str):

        try:
            statement = select(Book).where(Book.id == book_uid)     
            result = await self.session.exec(statement)
            book = result.first()
        except:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f'Invalid id: {book_uid}')
        if not book:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                                detail= f'Book con id: {book_uid} does not exist')
        if book.owner_id != current_user:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                                detail= f'Not authorized to perform action')
        return book

    async def create_book(self, book_data: BookCreate, current_user: str):
        
        new_book = Book (owner_id = current_user, **book_data.model_dump())
        self.session.add(new_book)
        await self.session.commit()
        await self.session.refresh(new_book)
        return new_book
    
    async def update_book(self, book_uid: str, book_update_data:BookCreate, current_user: str):

        try:
            statement = select(Book).where(Book.id == book_uid)
            result = await self.session.exec(statement)
            book = result.first()

        except:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f'Invalid id: {book_uid}')
        if not book:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                                detail= f'Book con id: {book_uid} does not exist')
        if book.owner_id != current_user:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                                detail= f'Not authorized to perform action')
        
        for key,value in book_update_data.model_dump().items():
            setattr (book, key, value)
        
        await self.session.commit()
        return book

    async def delete_book(self, book_uid: str, current_user):

        try:
            statement = select(Book).where(Book.id == book_uid)
            result = await self.session.exec(statement)
            book = result.first()
        except:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f'Invalid id: {book_uid}')
        if not book:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                                detail= f'Book con id: {book_uid} does not exist')
        if book.owner_id != current_user:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                                detail= f'Not authorized to perform action')
        
        await self.session.delete(book)
        await self.session.commit()





