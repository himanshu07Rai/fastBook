from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import Column, Integer
from datetime import datetime
import uuid
from typing import List

from src.books import models
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
    books: List["models.Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}) # lazy="selectin" is used to load the relationship in the same query as the parent object. This is useful when you know you will need the related object and want to avoid the N+1 query problem.
    
    def __repr__(self):
        return f"User {self.username}"