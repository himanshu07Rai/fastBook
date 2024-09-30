from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    username: str
    password: str = Field(exclude=True)
    email: str
    first_name: str
    last_name: str
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def __repr__(self):
        return f"User {self.username}"
    
    def __repr__(self) -> str:
        return f"User {self.username}"