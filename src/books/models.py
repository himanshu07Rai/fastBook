from datetime import datetime, date
from sqlmodel import Field, SQLModel, Relationship
import uuid
from typing import Optional
from src.auth import models


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
    user: Optional["models.User"] = Relationship(back_populates="books")
    def __repr__(self):
        return f"Book {self.title}"
