from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
import json

host = os.getenv("HOST" ,"localhost")
port = os.getenv("PORT" ,27017)
user = os.getenv("USER" ,"kodi")
password = os.getenv("PASSWORD" ,"word")
uri = f"mongodb://{user}:{password}@{host}:{port}"

class MongoService:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        try:
            self.client = MongoClient(uri)
            print(uri)
            self.client.admin.command('ping')
            print("connection established")
        except ConnectionFailure as e:
            print(f"connection failed")
            raise e
        
    def create_collection(self):
        self.db = self.client['pizza_db']
        self.collection = self.db['pizza_collection']
        return self.collection
        
    def update(self, select, new_value):
        try:
            result = self.collection.update_one(select, new_value)
            return result
        except Exception as e:
            print("update failed")
            raise e
        
