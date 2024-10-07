import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReviewSchema(BaseModel):
    id: uuid.UUID
    rating: int = Field(lt=5)
    review: str
    user_id: Optional[uuid.UUID]
    book_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime


class ReviewCreateSchema(BaseModel):
    rating: int = Field(lt=5)
    review: str
