from pydantic import BaseModel, Field
import uuid
from datetime import datetime, date
from typing import List
from src.books.schema import BookSchema
from src.reviews.schema import ReviewSchema

class UserCreateSchema(BaseModel):
    username: str = Field(max_length=8)
    email: str = Field(max_length=50)
    password: str = Field(max_length=10)
    first_name: str
    last_name: str

class UserSchema(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    password: str = Field(exclude=True)
    first_name: str
    last_name: str
    is_verified: bool
    role: int
    created_at: datetime
    updated_at: datetime

class UserWithBooksSchema(UserSchema):
    books: List[BookSchema]
    reviews: List[ReviewSchema]

class UserLoginSchema(BaseModel):
    email: str
    password: str