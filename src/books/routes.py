from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schema import BookCreateModel
from src.db.main import get_session
from .service import BookService

router = APIRouter()
book_service = BookService()

@router.get('/')
async def get_books(session:AsyncSession = Depends(get_session)):
    books =await book_service.get_all_books(session)
    return books

@router.get('/{id}')
async def get_book_by_id(id: int) -> dict:
    print(id)
    for book in books:
        if book['id'] == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)):
    new_book = await book_service.create_book(book_data, session)
    return new_book

