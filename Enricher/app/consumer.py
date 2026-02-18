import json

from confluent_kafka import Consumer

consumer_config = {
    "bootstrap.servers": "kafka:9092",
    "group.id": "enricher-tracker",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_config)



def get_data_from_kafka():
        msg = consumer.poll(1.0)
        if msg is None:
            return None
        if msg.error():
            print("❌ Error:", msg.error())
            return None

        value = msg.value().decode("utf-8")
        data = json.loads(value)
        return data

