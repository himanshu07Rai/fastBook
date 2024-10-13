import redis
from src.config import Config

client = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)

def get_redis_client():
    return client

def get_client() -> redis.Redis:
    return get_redis_client()