import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from app.main import app
from app.helper import load_json, save_json

client = TestClient(app)

test_fund = {
    "fund_id": "test001",
    "fund_name": "Test Fund",
    "manager_name": "Test Manager",
    "desc": "A test fund",
    "net_asset": 1000000.0,
    "created_at": "2024-08-22T14:30:00Z",
    "performance": 5.0
}

TEST_FILE = Path.cwd() / "temp_db.json"

@pytest.fixture(autouse=True)
def setup_and_teardown():
    save_json(TEST_FILE, [test_fund])
    yield 
    save_json(TEST_FILE, [])

def setup():
    data = load_json(TEST_FILE)
    assert len(data) == 0

def test_save_json():
    new_data = [test_fund]
    save_json(TEST_FILE, new_data)
    loaded_data = load_json(TEST_FILE)
    assert len(loaded_data) == 1
    assert loaded_data[0]['fund_id'] == test_fund["fund_id"]

def test_get_funds():
    response = client.get("/get-funds")
    assert response.status_code == 201
    assert len(response.json()) == 1
    assert response.json()[0]['fund_id'] == test_fund["fund_id"]

def test_create_fund():
    new_fund = test_fund.copy()
    new_fund['fund_id'] = "test002"
    new_fund['fund_name'] = "New Test Fund"
    response = client.post("/create-fund", json=new_fund)
    assert response.status_code == 200
    assert response.json()['message'] == "Successfully created new fund"
    
    get_response = client.get("/get-funds")
    assert len(get_response.json()) == 2

def test_get_one_fund():
    response = client.get(f"/get-one-fund/{test_fund['fund_id']}")
    assert response.status_code == 200
    assert response.json()['fund_id'] == test_fund['fund_id']

def test_update_fund_performance():
    new_performance = 8.0
    response = client.patch(f"/update-fund/{test_fund['fund_id']}?performance={new_performance}")
    assert response.status_code == 200
    assert response.json()['message'] == "Successfully updated fund performance"

    get_response = client.get(f"/get-one-fund/{test_fund['fund_id']}")
    assert get_response.json()['performance'] == new_performance

def test_delete_fund():
    response = client.delete(f"/remove-fund/{test_fund['fund_id']}")
    assert response.status_code == 200
    assert response.json()['message'] == "Successfully deleted fund"

def test_error_handling():
    response = client.post("/create-fund", json=test_fund)
    assert response.status_code == 400

    response = client.get("/get-one-fund/nonexistent")
    assert response.status_code == 404

    response = client.patch("/update-fund/nonexistent?performance=5.0")
    assert response.status_code == 404

    response = client.delete("/remove-fund/nonexistent")
    assert response.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__])
