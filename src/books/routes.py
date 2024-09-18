from fastapi import APIRouter, HTTPException, Header

from .books_data import books

router = APIRouter()

@router.get('/')
def get_books() -> list:
    return books

@router.get('/{id}')
def get_book_by_id(id: int) -> dict:
    print(id)
    for book in books:
        if book['id'] == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")



