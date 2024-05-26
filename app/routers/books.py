from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.db.database import get_session
from app.db.schemas import BookResponse, BookCreate, BookVoteResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from app.routers.books_service import BookService
from typing import List
from app.authentication.oauth2 import get_current_user

router = APIRouter (prefix='/books', tags=['Books'])

@router.get('/', response_model=List[BookVoteResponse])
async def get_books(db: AsyncSession = Depends(get_session)):
    
    books = await BookService(db).get_all_books()
    return books 


@router.get('/{book_id}', status_code=status.HTTP_200_OK)
async def get_book(book_id: str, db: AsyncSession = Depends(get_session),
                   current_user: str= Depends(get_current_user)):
    
    book = await BookService(db).get_one_book(book_id, current_user)
    return book

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_book(book_create: BookCreate, db: AsyncSession = Depends(get_session),
                      current_user: str= Depends(get_current_user)):
    
    new_book = await BookService(db).create_book(book_create, current_user)
    return new_book


@router.put('/{book_id}', status_code=status.HTTP_200_OK)
async def update_book(book_id: str, updated_data:BookCreate, db: AsyncSession= Depends(get_session),
                      current_user: str= Depends(get_current_user)):
    
    updated_book = await BookService(db).update_book(book_id, updated_data, current_user)
    return updated_book

@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, db: AsyncSession = Depends(get_session),
                      current_user: str= Depends(get_current_user)):
    
    await BookService(db).delete_book(book_id, current_user)
    return Response (status_code=status.HTTP_204_NO_CONTENT)

