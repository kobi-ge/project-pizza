from consumer import consumer
import time
import json

from redis_connection import ConnectRedis
from utils import delete_from_redis
from mongo_connection import MongoService
from confluent_kafka import Consumer



consumer.subscribe(["pizza-orders"])

print("🟢 kitchen consumer is running and subscribed to orders topic")

client = MongoService()
client.connect()
collection = client.create_collection()
r = ConnectRedis()
r = r.connect()
print('asdff')



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
        delete_from_redis(order['order_id'], r)
        print("data deleted from redis")
        client.update({"order_id": order['order_id']}, {"$set": {"status": "DELIVERED"}})
        print(f"order: {order['order_id']} cache was deleted from redis and updated version sent to mongo")
        time.sleep(15)
except KeyboardInterrupt:
    print("\n🔴 Stopping kitchen consumer")
    consumer.close()

