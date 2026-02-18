from utils import *
from consumer import get_data_from_kafka, consumer
from mongo_connection import MongoService

client = MongoService()
client.connect()
collection = client.create_collection()

consumer.subscribe(["cleaned-instructions"])

print("🟢 Enricher consumer is running and subscribed to orders topic")

def main():
    try:
        while True:
            data = get_data_from_kafka()
            if not data: 
                print("data is none")
                continue
            data = set_keys(data)
            text = data["pizza_prep"]
            analysis_data = read_from_file("data/pizza_analysis_lists.json")
            lists = split_to_lists(analysis_data)
            for current_list, key in zip(lists, keys):
                changed = False
                result = compatibility_check(current_list, text)
                if result and not changed:
                    data[key] = not(data[key])
                    changed = True
            if check_vegan_or_gluten(text, "VEGAN"):
                data['vegan'] = True
            if check_vegan_or_gluten(text, "GLUTEN-FREE"):
                data['gluten_free'] = True
            data = determine_kosher(data)
            print(data)
            client.update({"order_id": data['order_id']}, {"$set": {
                    'is_alergan': data['is_alergan'], 
                    'is_kosher': data['is_kosher'],
                    'is_meat': data['is_meat'],
                    'is_dairy': data['is_dairy'],
                    'status': data['status'],
                    'pizza_prep': data['pizza_prep'],
                    'special_instructions': data['special_instructions']
            }})
            print(f"finished updating keys for order: {data['order_id']} and sent updates to mongo")
    except KeyboardInterrupt:
        print("\n🔴 Stopping consumer")
        consumer.close()

main()

