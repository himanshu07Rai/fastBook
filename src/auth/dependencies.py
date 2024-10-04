from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from fastapi import Request, status
from fastapi.exceptions import HTTPException

from .utils import decode_token

class AccessTokenBearer(HTTPBearer):
    # def __init__(self, auto_error: bool = True):
    #     super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request)->Optional[HTTPAuthorizationCredentials]:
        credentials = await super().__call__(request)
        is_token_valid, token_payload = self.is_token_valid(credentials.credentials)
        if not is_token_valid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        if token_payload['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh token not allowed",
            )

        return token_payload

    def is_token_valid(self, token: str) -> tuple:
        token_payload = decode_token(token)
        return token_payload is not None, token_payload
