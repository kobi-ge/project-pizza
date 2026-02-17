from consumer import consumer
import time
import json

from mongo_connection import MongoService
from utils import *
from producer import produce_to_kafka


consumer.subscribe(["pizza-orders"])

print("🟢 Preprocessor consumer is running and subscribed to orders topic")

client = MongoService()
client.connect()
collection = client.create_collection()


def main():
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
            cleaned_special_instructions = clearing_the_data(order['special_instructions'])
            prep_data = read_from_file("data/pizza_prep.json")
            current_prep = get_prep_by_type(prep_data, order['pizza_type'])
            cleaned_current_prep = clearing_the_data(current_prep)
            print(f"cleaned special instructions for order {order['order_id']} and prep instructions for current pizza type") 
            data_teady = get_structure_data(order, order['pizza_type'], cleaned_special_instructions, cleaned_current_prep)
            produce_to_kafka(data_teady)
            print(f"order: {order['order_id']} was sent to kafka with updated fields")
    except KeyboardInterrupt:
        print("\n🔴 Stopping kitchen consumer")
        consumer.close()

main()