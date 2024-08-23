import json

from pathlib import Path
from typing import List, Dict

# Helper functions that read and write to JSON file
def load_json(file_path: str) -> List[Dict]:
    '''
        Loads JSON file according to specified path.
        Args:
            - file_path (str): JSON file path
        Returns: 
            - list of fund objects
    '''
    try:
        with open(Path(file_path), "r") as f:
            return json.load(f)
        
    except FileNotFoundError:
        return {}
    
def save_json(file_path: str, data: dict) -> None:
    '''
        Persists JSON data for fund records according to API operations.
        Args: 
            - file_path (str): JSON file path
            - data (dict): fund data to be written into JSON
    '''
    try:
        with open(Path(file_path), "w") as f:
            json.dump(data, f, default=str)

    except Exception as e:
        raise IOError(f"Error saving JSON data: {e}")