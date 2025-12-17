import redis

from settings import settings

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=2,
    decode_responses=True,
)


def already_processed(key: str) -> bool:
    return r.exists(key) == 1


def mark_processed(key: str):
    r.set(key, "1")
