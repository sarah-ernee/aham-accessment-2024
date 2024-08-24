import json
import csv

from pathlib import Path

FILE_DIR = Path.cwd() / "temp_db.json"

with open(FILE_DIR) as json_file:
    data = json.load(json_file)

CSV_PATH = Path.cwd() / "temp_db.csv"

with open(CSV_PATH, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
    writer.writeheader()
    for entry in data:
        writer.writerow(entry)
