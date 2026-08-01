import redis

from rq import Queue


redis_connection = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
)


scan_queue = Queue(
    "scan",
    connection=redis_connection,
)