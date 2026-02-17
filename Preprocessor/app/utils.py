import string
import json


def search_in_text(data):
    if "allergy" in data["special_instructions"].lower() or \
            "peanut" in data["special_instructions"].lower() or\
            "gluten" in data["special_instructions"].lower():
        data["allergies_flagged"] = True
    else:
        data["allergies_flagged"] = False

    return data


def clearing_the_data(data):
    translator = str.maketrans('', '', string.punctuation)
    clean_text = data.translate(translator)
    data = clean_text.upper()
    return data

def read_from_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
        return data

def get_prep_by_type(data, type):
    return data.get(type, '')


def get_structure_data(order, pizza_type, inrctns, prep):
    return {
        "order_id": order['order_id'],
        "pizza_type": order["pizza_type"],
        "special_instructions": inrctns,
        "pizza_prep": prep
    }