import redis
from redis import RedisError
import os


host = os.getenv("REDIS_HOST")
port = int(os.getenv("REDIS_PORT"))


class ConnectRedis:
    def __init__(self):
        self.r = None

    def connect(self):
        self.r = redis.Redis(host=host, port=port, db=0)
        return self.r
    