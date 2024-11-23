from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.config import Config
import jwt
import uuid
import logging
from src.db.redis import get_client
from itsdangerous import URLSafeTimedSerializer


ACCESS_TOKEN_EXPIRY = 3600

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh:bool = False) -> str:
    payload = {}
    payload['user_data'] = user_data
    payload['exp'] = datetime.now() + (expiry or timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    encoded_jwt = jwt.encode(
        payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM)
    return encoded_jwt, payload['jti']

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
serializer = URLSafeTimedSerializer(Config.JWT_SECRET,"email-confirm")

def create_confirmation_token(user_data: dict) -> str:
    
    token = serializer.dumps(user_data)
    return token

def verify_confirmation_token(token: str, max_age:int = 3600) -> dict: # 1 hour
    try:
        user_data = serializer.loads(token, max_age=max_age)
        return user_data
    except Exception as e:
        logging.exception(e)
        return None
    