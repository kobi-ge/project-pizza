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
    
    def insert(self, value):
        try:
            result = self.collection.insert_one(value)
            return result
        except Exception as e:
            print("insertion failed")
            raise e
        
    def get_data(self, order_id):
        query = {"order_id": order_id}
        result = self.collection.find(query).to_list()
        result[0]['_id'] = str(result[0]['_id'])
        result[0]['uuid'] = str(result[0]['uuid'])
        return result[0]