import json

def read_json(filepath):
    """
    Read and parse a JSON file.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON data.
    """
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        print(f"JSON successfully read from {filepath}")
        return data
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {filepath}: {e}")
        return None


def write_json(data, filepath):
    """
    Write data to a JSON file.

    Args:
        data (dict): Data to write.
        filepath (str): Path to the JSON file.
    """
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"JSON successfully written to {filepath}")
    except IOError as e:
        print(f"Error writing JSON to {filepath}: {e}")

