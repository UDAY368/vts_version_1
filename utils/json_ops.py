# all the constant values in the software
import json
def store_default_value_dict(default_value_dict):
    # Perform operations (e.g., modifying or accessing dictionary)
    print("Received dictionary:", default_value_dict)
    
    # Export the dictionary to a JSON file
    export_to_json(default_value_dict, 'default_values/default_values.json')

def export_to_json(data, filename):
    # Writing the dictionary to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)  # indent=4 for pretty formatting
    print(f"Dictionary has been exported to {filename}")

def load_json_from_file(file_path):
    # Open the JSON file and load its content
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data