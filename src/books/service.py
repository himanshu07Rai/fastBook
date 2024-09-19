from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schema import BookCreateModel
from .models import Book
from datetime import datetime

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(Book.created_at)
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_id:str, session: AsyncSession):
        statement = select(Book).where(Book.id == book_id)
        result = await session.exec(statement)
        return result.first()

    async def create_book(
        self, book_data: BookCreateModel, session: AsyncSession
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