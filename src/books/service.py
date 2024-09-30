from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schema import BookCreateSchema, BookUpdateSchema
from .models import Book
from datetime import datetime
import uuid

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(Book.created_at)
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_id:str, session: AsyncSession):
        if is_valid_uuid(book_id):
            book_id = uuid.UUID(book_id)
        else:
            return None
        statement = select(Book).where(Book.id == book_id)
        result = await session.exec(statement)
        book = result.first() 
        if book is None:
            return None
        return book

    async def create_book(
        self, book_data: BookCreateSchema, session: AsyncSession
    ):
        try:
            book_data_dict = book_data.model_dump()
            book_data_dict['published_date'] = datetime.strptime(book_data_dict['published_date'],"%Y-%m-%d").date()
            new_book = Book(**book_data_dict)
            session.add(new_book)
            await session.commit()
            return new_book
        except Exception as e:
            print(e)
            await session.rollback()
            return None

    async def update_book(
        self, book_id: str, update_data: BookUpdateSchema, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_id, session)
        if book_to_update is not None:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(book_to_update, k, v)
            await session.commit()
            return book_to_update
        else:
            return None

    async def delete_book(self, book_uid: str, session: AsyncSession)-> dict:
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return book_to_delete
        else:
            return None