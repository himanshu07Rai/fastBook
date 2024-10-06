from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta, datetime
from .schema import UserCreateSchema, UserSchema, UserLoginSchema
from .service import UserService
from src.db.main import get_session
from .utils import create_access_token, verify_password
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user
from src.db.redis import get_client
from src.konstants import VALID_ACCESS_TOKEN_IDS

auth_router = APIRouter()
auth_service = UserService()
user_data_from_refresh_token = RefreshTokenBearer()
access_token_details = AccessTokenBearer()

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def signup(user_data: UserCreateSchema, session:AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await auth_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = await auth_service.create_user(user_data, session)
    return new_user

@auth_router.post('/login')
async def login(user_data: UserLoginSchema, session:AsyncSession = Depends(get_session), client=Depends(get_client)):
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
        "role": user.role
    }
    access_token, jti = create_access_token(user_data)
    refresh_token = create_access_token(user_data, refresh=True, expiry=timedelta(days=30))
    client.sadd(VALID_ACCESS_TOKEN_IDS, jti)
    return {
        "user": {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role
        },
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@auth_router.post('/refresh')
async def get_new_access_token(user_token_data:dict= Depends(user_data_from_refresh_token)):
    expiry_timestamp = user_token_data['exp']
    user_data = user_token_data['user']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        access_token = create_access_token(user_data)
        return {
            "access_token": access_token
        }
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token")

@auth_router.get('/me', response_model=UserSchema)
async def get_current_user(user: dict = Depends(get_current_user)):
    return user

@auth_router.post('/logout')
async def logout(token_details: dict = Depends(access_token_details), client=Depends(get_client)):
    jti = token_details['jti']
    client.srem(VALID_ACCESS_TOKEN_IDS, jti)
    return {
        "message": "Successfully logged out"
   }