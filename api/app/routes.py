from fastapi import APIRouter, UploadFile, HTTPException
import json

from mongo_connection import MongoService
from utils import send_orders

client = MongoService()
client.connect()
collection = client.create_collection()

router = APIRouter()

@router.post("/uploadfile")
def upload_orders_file(file: UploadFile):
    data_json = file.file.read()
    data = json.loads(data_json)
    send_orders(data, client)



