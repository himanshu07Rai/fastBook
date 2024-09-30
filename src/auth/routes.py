from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schema import UserCreateSchema, UserSchema
from .service import UserService
from src.db.main import get_session

auth_router = APIRouter()
auth_service = UserService()

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def signup(user_data: UserCreateSchema, session:AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await auth_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = await auth_service.create_user(user_data, session)
    return new_user
