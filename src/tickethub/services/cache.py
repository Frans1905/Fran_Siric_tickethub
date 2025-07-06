import redis.asyncio as redis
from tickethub.config import settings

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
