from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import Column, Integer
from datetime import datetime, date
import uuid
from typing import List, Optional
from src.konstants import USER_ROLE

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    username: str
    password: str = Field(exclude=True)
    email: str
    first_name: str
    last_name: str
    is_verified: bool = False
    role: int = Field(
        default=USER_ROLE['NORMAL'],
        sa_column=Column(Integer, server_default=str(USER_ROLE['NORMAL']), nullable=False)
    ) # using server_default sets the default value at the database level for both existing rows (when adding the column) and for new rows if the column is not explicitly set. However, this only affects the database layer. When using SQLModel to create new entries, you might need to set the Python-level default as well to maintain consistency.
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    books: List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}) # lazy="selectin" is used to load the relationship in the same query as the parent object. This is useful when you know you will need the related object and want to avoid the N+1 query problem.
    reviews: List["Review"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    # def __repr__(self):
    #     return f"Userhhh {self.username}"
    


class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy": "selectin"})
    # def __repr__(self):
    #     return f"Book {self.title}"
    
class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    book_id: Optional[uuid.UUID] = Field(default=None, foreign_key="books.id") 
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    rating: int = Field(default=0, ge=0, le=5)
    review: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    book: Optional["Book"] = Relationship(back_populates="reviews")
    user: Optional["User"] = Relationship(back_populates="reviews")
    def __repr__(self):
        return f"Review {self.id} from {self.user_id} for {self.book_id}"