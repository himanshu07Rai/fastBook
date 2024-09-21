from datetime import datetime, date
from sqlmodel import Field, SQLModel


import uuid


class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def __repr__(self):
        return f"Book {self.title}"
