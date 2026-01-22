from redis import Redis
from rq import Queue
from app.settings import settings

redis_conn = Redis.from_url(settings.REDIS_URL)
queue = Queue("default", connection=redis_conn)

def enqueue(fn, *args, **kwargs):
    return queue.enqueue(fn, *args, **kwargs)