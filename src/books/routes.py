from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schema import BookCreateSchema, BookUpdateSchema, BookDetailSchema
from src.db.main import get_session
from .service import BookService
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.db.redis import get_client
from src.konstants import VALID_ACCESS_TOKEN_IDS
from src.konstants import USER_ROLE

router = APIRouter()
book_service = BookService()
access_token_details = AccessTokenBearer() # similar to attach user
admin_role_checker = Depends(RoleChecker(USER_ROLE['ADMIN']))

@router.get('/', dependencies=[admin_role_checker])
async def get_all_books(session:AsyncSession = Depends(get_session), user_details: dict = Depends(access_token_details), redis_client = Depends(get_client)):
    if(redis_client.sismember(VALID_ACCESS_TOKEN_IDS, user_details['jti'])):
        books =await book_service.get_all_books(session)
        return books
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
        "message": "Invalid token",
        "resolve": "Please login again"
    })

@router.get('/user/{user_id}')
async def get_user_all_books(user_id:str, session:AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_details)):
    current_user_id = token_details['user_data']['id']
    books =await book_service.get_user_all_books(session, user_id, current_user_id)
    return books

@router.get('/{book_id}', response_model=BookDetailSchema)
async def get_book_by_id(book_id: str, session:AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_id,session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_a_book(
        book_data: BookCreateSchema,
        session: AsyncSession = Depends(get_session),
        token_details: dict = Depends(access_token_details)
    ):
    new_book = await book_service.create_book(book_data, session, user_id=token_details['user_details']['id'])
    return new_book

@router.put('/{book_id}', response_model=BookDetailSchema)
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

