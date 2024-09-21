from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schema import BookSchema, BookCreateSchema, BookUpdateSchema
from src.db.main import get_session
from .service import BookService

router = APIRouter()
book_service = BookService()

@router.get('/')
async def get_books(session:AsyncSession = Depends(get_session)):
    books =await book_service.get_all_books(session)
    return books

@router.get('/{book_id}', response_model=BookSchema)
async def get_book_by_id(book_id: str, session:AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_id,session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookCreateSchema, session: AsyncSession = Depends(get_session)):
    new_book = await book_service.create_book(book_data, session)
    return new_book

@router.put('/{book_id}', response_model=BookSchema)
async def update_a_book(book_id: str, book_data: BookUpdateSchema, session: AsyncSession = Depends(get_session)):
    updated_book = await book_service.update_book(book_id, book_data, session)
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return updated_book

@router.delete('/{book_id}' )
async def delete_a_book(book_id: str, session: AsyncSession = Depends(get_session))-> dict:
    deleted_book = await book_service.delete_book(book_id, session)
    if not deleted_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return {}

