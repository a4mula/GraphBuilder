import json

def save_file(data, filepath):
    """
    Save data to a file in JSON format.
    
    Args:
        data (dict or list): The data to save.
        filepath (str): The file path where the data will be saved.
    """
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data successfully saved to {filepath}")
    except IOError as e:
        print(f"Error saving file {filepath}: {e}")

def load_file(filepath):
    """
    Load data from a JSON file.
    
    Args:
        filepath (str): The file path to load data from.
        
    Returns:
        dict or list: The loaded data.
    """
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        print(f"Data successfully loaded from {filepath}")
        return data
    except IOError as e:
        print(f"Error loading file {filepath}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {filepath}: {e}")
        return None

