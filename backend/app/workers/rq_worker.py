import os
from rq import Worker
from app.infrastructure.queue.rq import queue, redis_conn

if __name__ == "__main__":
    # listen on the same queue your enqueue() uses
    Worker([queue], connection=redis_conn).work()
