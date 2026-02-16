from fastapi import APIRouter, UploadFile, HTTPException
import os
import json

from mongo_connection import MongoService
from utils import send_orders
from redis_connection import ConnectRedis

client = MongoService()
client.connect()
collection = client.create_collection()
r = ConnectRedis()
r.connect()


router = APIRouter()

@router.post("/uploadfile")
def upload_orders_file(file: UploadFile):
    data_json = file.file.read()
    data = json.loads(data_json)
    send_orders(data, client)
    return "data sent to mongo and kafka succussfully"


@router.get("/order/{order_id}")
def get_order(order_id: str):
    result = r.get_data(order_id)
    if result:
        print("cahce hit")
        return {
            "result": json.loads(result),
            "source": "redis"
        }
    print("cache miss")
    result = client.get_data(order_id)
    r.insert(order_id, result)
    return {
            "result": result,
            "source": "mongodb"
        }

    
