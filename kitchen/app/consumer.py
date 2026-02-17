from confluent_kafka import Consumer


consumer_config = {
    "bootstrap.servers": "kafka:9092",
    "group.id": "kitchen-team",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_config)



