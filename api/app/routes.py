from fastapi import APIRouter, UploadFile, HTTPException
import json

router = APIRouter()

@router.post("/uploadfile")
def upload_orders_file(file: UploadFile):
    data_json = file.file.read()
    data = json.loads(data_json)
    return data



