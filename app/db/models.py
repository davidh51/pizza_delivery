from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from sqlalchemy.sql.expression import text
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id: Mapped[UUID]= mapped_column(primary_key=True, unique=True, default=uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    author:Mapped[str] = mapped_column(nullable=False)
    isbn: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=text('now()'))
    updated_at: Mapped[datetime] = mapped_column(default=text('now()'))
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), 
                                          nullable=False)#Cascade que pasa con el post cuando el user 
                                                         # es eliminado
    
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID]= mapped_column(primary_key=True, unique=True, default=uuid4)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password :Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=text('now()'), nullable=False)

class Vote (Base):
    __tablename__="votes"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    book_id: Mapped[UUID] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)


