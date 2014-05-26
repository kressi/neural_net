import os
import redis

redis_url = os.getenv('REDISCLOUD_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)

