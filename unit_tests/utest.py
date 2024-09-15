# test_main.py
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from src.main import app, CarReport

client = TestClient(app)

@pytest.mark.asyncio
async def test_submit_car_report_valid():
    # Simulate a valid car report submission for a known car
    car_report = {
        "id": "b658bd54-7cbe-4342-aca3-b08bbf9f7f5d",  # Dacia Duster
        "car_model": "Dacia Duster",
        "fuel_type": "gas",
        "mileage": 100,
        "used_fuel": 5.4
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/car-report", json=car_report)

    assert response.status_code == 202
    assert response.json() == {"message": "Car status report accepted"}


@pytest.mark.asyncio
async def test_submit_car_report_invalid():
    # Simulate an invalid car report (wrong fuel consumption)
    car_report = {
        "id": "b658bd54-7cbe-4342-aca3-b08bbf9f7f5d",  # Dacia Duster
        "car_model": "Dacia Duster",
        "fuel_type": "gas",
        "mileage": 100,
        "used_fuel": 10.0  # Incorrect fuel consumption
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/car-report", json=car_report)

    assert response.status_code == 202
    assert response.json() == {"message": "Car status report accepted"}  # Response remains the same; validation happens internally


@pytest.mark.asyncio
async def test_submit_car_report_car_not_found():
    # Simulate a car report for a car that does not exist
    car_report = {
        "id": "non-existent-id",
        "car_model": "Non Existent Car",
        "fuel_type": "gas",
        "mileage": 100,
        "used_fuel": 5.0
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/car-report", json=car_report)

    assert response.status_code == 404
    assert response.json() == {"message": "Car not found"}


def test_health_check():
    # Test the health check endpoint
    response = client.get("/healthz")
    assert response.status_code == 204
