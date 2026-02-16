import uuid

from kafka_producer import produce_to_kafka

def send_orders(data, client):
    try:
        for order in data:
            order['status'] = "preparing"
            order['uuid'] = uuid.uuid4().bytes
            client.insert(order)
            print(f"order: {order['order_id']} inserted to collection")
            produce_to_kafka(order)
            print(f"order: {order['order_id']} sent to kafka")
        return "data sent succussfuly"
    except Exception as e:
        raise e
    


