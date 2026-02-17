import redis
from redis import RedisError
import os
import json


host = os.getenv("REDIS_HOST")
port = int(os.getenv("REDIS_PORT"))


class ConnectRedis:
    def __init__(self):
        self.r = None

    def connect(self):
        self.r = redis.Redis(host=host, port=port, db=0)
        return self.r
    
    def insert(self, key, value):
        try:
            self.r.set(key , value=json.dumps(value, default=str), ex=36000)
        except RedisError as e:
            print("error inserting to redis")
            raise e
        
    def get_data(self, key):
        data = self.r.get(key)
        return data
