from pydantic import BaseModel
import uuid
from datetime import datetime, date
from src.reviews.schema import ReviewSchema
from typing import List

class BookSchema(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime
    
class BookDetailSchema(BookSchema):
    reviews: List[ReviewSchema]


class BookCreateSchema(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateSchema(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str