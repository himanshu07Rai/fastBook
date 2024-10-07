from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from fastapi import Request, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from .utils import decode_token
from .service import UserService
from .schema import UserSchema
from src.errors import InvalidToken, RefreshTokenRequired, AccessTokenRequired, InsufficientPermission, AccountNotVerified


user_service = UserService()
# the below functions will check the tokrn and verify the token data
# if the token is valid, it will return the token payload
# if the token is invalid, it will raise an HTTPException with status code 403
# if the token is valid but the token data is not as expected, it will raise an HTTPException with status code 403
# if the token is valid and the token data is as expected, it will return the token payload, which is the user data

class TokenBearer(HTTPBearer):
    # def __init__(self, auto_error: bool = True):
    #     super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request)->Optional[HTTPAuthorizationCredentials]:
        credentials = await super().__call__(request)
        is_token_valid, token_payload = self.is_token_valid(credentials.credentials)
        if not is_token_valid:
            raise InvalidToken()
        self.verify_token_payload(token_payload)
        return token_payload

    def is_token_valid(self, token: str) -> tuple:
        token_payload = decode_token(token)
        return token_payload is not None, token_payload
    
    def verify_token_payload(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")
    
class AccessTokenBearer(TokenBearer):
    def verify_token_payload(self, token_payload):
        if token_payload and token_payload['refresh']:
            raise AccessTokenRequired()
    
class RefreshTokenBearer(TokenBearer):
    def verify_token_payload(self, token_payload):
        print(token_payload)
        if token_payload and not token_payload['refresh']:
            raise RefreshTokenRequired()

async def get_current_user(
        token: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session),
    ) -> UserSchema:
    user_email = token['user_data']['email']
    user = await user_service.get_user_by_email(user_email, session)
    return user

class RoleChecker:
    def __init__(self, role):
        self.role = role

    async def __call__(self, user: UserSchema = Depends(get_current_user)):
        print(user)
        if user.role < self.role:
            raise InsufficientPermission()
        return user
