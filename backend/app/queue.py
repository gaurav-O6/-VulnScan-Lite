import os

import redis
from rq import Queue


redis_url = os.getenv("REDIS_URL")

print("=" * 60)
print("REDIS_URL =", repr(redis_url))
print("=" * 60)

if redis_url:
    redis_connection = redis.from_url(redis_url)
else:
    redis_connection = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
    )

print("REDIS CONNECTION:", redis_connection)
print("CONNECTION KWARGS:", redis_connection.connection_pool.connection_kwargs)

scan_queue = Queue(
    "scan",
    connection=redis_connection,
)