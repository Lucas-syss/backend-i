from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI API!"}

def test_create_item_success():
    response = client.post("/items/", json={"name": "Test Item"})
    assert response.status_code == 200
    assert response.json() == {"item": {"name": "Test Item"}}

def test_create_item_failure():
    response = client.post("/items/", json={"description": "No name provided"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Item must have a name"

def test_update_item_success():
    client.post("/items/", json={"name": "Test Item", "price": 100})
    response = client.put("/items/1", json={"name": "Updated Item", "price": 150})
    assert response.status_code == 200
    assert response.json() == {"message": "Item updated successfully", "item": {"name": "Updated Item", "price": 150}}

def test_update_item_failure():
    response = client.put("/items/999", json={"name": "Non-Existent Item", "price": 50})
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
    
def test_delete_item_success():
    response = client.delete("/items/1")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {"message": "Item deleted successfully", "item": {"name": "Updated Item", "price": 150}}

def test_delete_item_failure():
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"