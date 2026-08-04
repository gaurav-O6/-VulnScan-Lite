import os

import redis
from rq import Queue


redis_url = os.getenv("REDIS_URL")

if redis_url:
    redis_connection = redis.from_url(
        redis_url,
        ssl=True,
        ssl_cert_reqs=None,
    )
else:
    redis_connection = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
    )

scan_queue = Queue(
    "scan",
    connection=redis_connection,
)