from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from fastapi import Request, status
from fastapi.exceptions import HTTPException

from .utils import decode_token

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
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
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
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh token not allowed",
            )
    
class RefreshTokenBearer(TokenBearer):
    def verify_token_payload(self, token_payload):
        print(token_payload)
        if token_payload and not token_payload['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access token not allowed",
            )
