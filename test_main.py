import pytest
from fastapi.testclient import TestClient
from main import app, add

client = TestClient(app)

# 🔹 Fixture (reusable data)
@pytest.fixture
def student_data():
    return {
        "name": "Rahul",
        "age": 22,
        "course": "AI"
    }

# ✅ Test: Create student API
def test_create_student(student_data):
    response = client.post("/students", json=student_data)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["name"] == "Rahul"
    assert data["age"] == 22
    assert data["course"] == "AI"
    assert "id" in data   # id generate ho raha hai ya nahi

# ✅ Test: Get students API
def test_get_students():
    response = client.get("/students")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ✅ Test: Function
def test_add_function():
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-1, 1) == 0