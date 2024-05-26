from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from pydantic.types import conint
from typing import List, Dict, Tuple, Union


class BookResponse(BaseModel):
    id: UUID
    title: str
    author:str
    isbn: str
    description: str
    created_at: datetime
    updated_at: datetime
    owner_id: UUID

class BookVoteResponse(BaseModel):
    Book: BookResponse
    vote: int

class BookCreate(BaseModel):
    title: str
    author:str
    isbn: str
    description: str

    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "Python Book",
                "author" : "Jon Doe",
                "isbn" : "987654321",
                "description" : "Python Collection"
            }    
        }
    }

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    model_config = {
        "json_schema_extra":{
            "example":{
                "email": "jondeo@gmail.com",
                "password" : "123456"
            }    
        }
    }

class Token (BaseModel):
    access_token : str
    token_type: str

class TokenData (BaseModel):
    id: str

class PasswordReset(BaseModel):
    email: EmailStr

class NewPasssword(BaseModel):
    password: str

class VoteModel(BaseModel):
    book_id: str
    dir: conint(le=1) # solo permite valores menores a 1

