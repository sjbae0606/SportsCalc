import json
import os

def save_data_to_file(data, filepath):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def load_data_from_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    return None
