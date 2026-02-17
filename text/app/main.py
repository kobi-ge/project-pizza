from consumer import consumer
import time
import json

from mongo_connection import MongoService
from utils import *


consumer.subscribe(["pizza-orders"])

print("🟢 kitchen consumer is running and subscribed to orders topic")

client = MongoService()
client.connect()
collection = client.create_collection()


try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("❌ Error:", msg.error())
            continue

        value = msg.value().decode('utf-8')
        order = json.loads(value)
        order = search_in_text(order)
        print(f"added fields to order {order['order_id']}")
        order = clearing_the_data(order)
        print(f"cleaned order {order['order_id']} from dots and colons")
        client.update({"order_id": order['order_id']}, {"$set": {"allergies_flagged":order["allergies_flagged"],  
                                                                 "cleaned_protocol": order["cleaned_protocol"]}})
        print(f"order: {order['order_id']} cache was deleted from redis and updated version sent to mongo")
except KeyboardInterrupt:
    print("\n🔴 Stopping kitchen consumer")
    consumer.close()

