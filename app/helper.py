import json

from pathlib import Path

def load_json(file_path: str):
    try:
        with open(Path(file_path), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}