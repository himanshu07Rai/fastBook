from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import RoleChecker, get_current_user
from src.db.main import get_session
from src.db.models import User
from src.konstants import USER_ROLE

from .schema import ReviewCreateSchema
from .service import ReviewService

review_service = ReviewService()
review_router = APIRouter()
admin_role_checker = Depends(RoleChecker(USER_ROLE['ADMIN']))
user_role_checker = Depends(RoleChecker(USER_ROLE['NORMAL']))


@review_router.get("/", dependencies=[admin_role_checker])
async def get_all_reviews(session: AsyncSession = Depends(get_session)):
    books = await review_service.get_all_reviews(session)

    return books


@review_router.get("/{review_id}", dependencies=[user_role_checker])
async def get_review(review_id: str, session: AsyncSession = Depends(get_session)):
    book = await review_service.get_review(review_id, session)

    if not book:
        raise HTTPException(
            detail="Review not found", status_code=status.HTTP_404_NOT_FOUND
        )


@review_router.post("/book/{book_id}", dependencies=[user_role_checker])
async def add_review_to_books(
    book_id: str,
    review_data: ReviewCreateSchema,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    new_review = await review_service.add_review_to_book(
        user_email=current_user.email,
        review_data=review_data,
        book_id=book_id,
        session=session,
    )

    return new_review


@review_router.delete(
    "/{review_id}",
    dependencies=[user_role_checker],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_review(
    review_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await review_service.delete_review_to_from_book(
        review_id=review_id, user_email=current_user.email, session=session
    )

    return None
