import json
import sys

def merge_data(old_data, new_data):
    for key, value in new_data.items():
        if value is not None:
            if key == "destination" and old_data.get("destination") is not None and old_data.get("destination_code") != -1:
                continue
            if key == "origin" and old_data.get("origin") is not None and old_data.get("origin_code") != -1:
                continue
            if (key == "destination_code" or key == "origin_code") and old_data.get(key) == -1:
                corresponding_key = "destination" if key == "destination_code" else "origin"
                if new_data.get(corresponding_key) is None or new_data.get(corresponding_key) == old_data.get(corresponding_key):
                    continue
            if key not in old_data or old_data[key] is None or old_data[key] in [-1, 0]:
                old_data[key] = value

    return old_data


def check_data(data):
    required_fields = ["money", "origin", "destination", "total_people", "date"]
    missing = [field for field in required_fields if not data.get(field)]
    
    if missing:
        response = f"Please provide values for the following fields: {', '.join(missing)}"
        data['time'] = 1
    else:
        if data.get('destination_code') == -1:
            response = "This travel does not fall within the service range in New Zealand. Chat ends."
            data['time'] = -1
        elif data.get('destination_code') == -2 and data.get('origin_code') == -1:
            response = "Based on your information, we are searching for the most suitable travel destinations.Please check your basic information first."
            data['time'] = 2
        elif data.get('destination_code') == -2 and data.get('origin_code') == 1:
            response = "Based on your information, we are searching for the most suitable travel destinations nearby.Please check your basic information first."
            data['time'] = 3
        elif data.get('destination_code') == 1 and data.get('origin_code') == 1 or -1:
            response = "Based on your information, we are retrieving dining and accommodation information for the location.Please check your basic information first."
            data['time'] = 4

    return f"{response}##{json.dumps(data)}"

def main():
    combined_data = json.loads(sys.argv[1])
    old_data = combined_data["old_data"]
    new_data = combined_data["new_data"]

    merged_data = merge_data(old_data, new_data)
    result = check_data(merged_data)

    print(result)

if __name__ == "__main__":
    main()
