import redis
from src.config import Config

client = redis.from_url(url=Config.REDIS_URL)

def get_redis_client():
    return client

def get_client() -> redis.Redis:
    return get_redis_client()