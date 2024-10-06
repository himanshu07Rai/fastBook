import redis

client = redis.Redis(host='localhost', port=6380, db=0)

def get_redis_client():
    return client

def get_client() -> redis.Redis:
    return get_redis_client()