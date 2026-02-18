import json

def read_from_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
        return data
    
def split_to_lists(data):
    common_allergens = data['common_allergens']
    forbidden_non_kosher = data['forbidden_non_kosher']
    meat_ingredients = data['meat_ingredients']
    dairy_ingredients = data['dairy_ingredients']
    return [common_allergens, forbidden_non_kosher, meat_ingredients, dairy_ingredients]

def set_keys(data):
    data['is_alergan'] = False
    data['is_kosher'] = True
    data['is_meat'] = False
    data['is_dairy'] = True
    data['status'] = "DELIVERED"
    return data

keys = ["is_alergan", "is_kosher", "is_meat", "is_dairy"]

def compatibility_check(current_list, text):
    for item in current_list:
        if item in text.lower():
            return True
    return False

def check_vegan_or_gluten(text, key):
    if key in text:
        return True
    return False

def determine_kosher(data):
    if not data['is_kosher']:
        data["status"] = "BURNT"
        return data
    if data["is_dairy"] and data["is_meat"]:
        data['is_kosher'] = False
        data["status"] = "BURNT"
    return data
    