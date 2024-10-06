from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Column, Integer
from datetime import datetime
import uuid

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
    
    def __repr__(self):
        return f"User {self.username}"