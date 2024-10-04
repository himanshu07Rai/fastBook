from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta
from .schema import UserCreateSchema, UserSchema, UserLoginSchema
from .service import UserService
from src.db.main import get_session
from .utils import create_access_token, verify_password

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

@auth_router.post('/login')
async def login(user_data: UserLoginSchema, session:AsyncSession = Depends(get_session)):
    email = user_data.email
    password = user_data.password
    user = await auth_service.get_user_by_email(email, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    user_data = {
        "id": str(user.id),
        "email": user.email,
    }
    access_token = create_access_token(user_data)
    refresh_token = create_access_token(user_data, refresh=True, expiry=timedelta(days=30))
    return {
        "user": {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name
        },
        "access_token": access_token,
        "refresh_token": refresh_token
    }