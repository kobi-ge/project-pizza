import json

from confluent_kafka import Producer

producer_config = {
    "bootstrap.servers": "kafka:9092"
}

producer = Producer(producer_config)

def delivery_report(err, msg):
    if err:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Delivered {msg.value().decode('utf-8')}")
        print(f"✅ Delivered to {msg.topic()} : partition {msg.partition()} : at offset {msg.offset()}")

def produce_to_kafka(order):
    value = json.dumps(order, default=str).encode("utf-8")

    producer.produce(
        topic="pizza-orders",
        value=value,
        callback=delivery_report
    )

    producer.flush()
