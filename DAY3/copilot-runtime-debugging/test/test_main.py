from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
# Test 1: TypeError fix
def test_calculate_bonus():
    response = client.get("/employee/bonus")
    assert response.status_code == 200
    assert response.json()["bonus"] == 5000.0


# Test 2: KeyError fix - Existing employee
def test_get_existing_employee():
    response = client.get("/employee/101")
    assert response.status_code == 200
    assert response.json()["name"] == "Rahul"
# Test 3: KeyError fix - Missing employee
def test_get_missing_employee():

    response = client.get("/employee/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee 999 not found"


# Test 4: ZeroDivisionError fix - Valid calculation
def test_average_salary():

    response = client.get(
        "/employee/average-salary",
        params={
            "total_salary": 150000,
            "employee_count": 3
        }
    )

    assert response.status_code == 200
    assert response.json()["average_salary"] == 50000.0


# Test 5: ZeroDivisionError fix - Zero employees
def test_zero_employee_count():

    response = client.get(
        "/employee/average-salary",
        params={
            "total_salary": 150000,
            "employee_count": 0
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Employee count must be greater than zero"
    )
