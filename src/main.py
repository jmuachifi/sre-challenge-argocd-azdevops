# main.py
#!/usr/bin/python3

"""
This module defines a FastAPI application for managing car reports,
validating fuel consumption, and providing health checks.
"""

import logging
import math
from typing import Optional

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

# Setup loggers
logging.basicConfig(
    format="[%(levelname)s - %(asctime)s] %(message)s", level=logging.INFO
)

# Get root logger
logger = logging.getLogger(__name__)

app = FastAPI()


class Car(BaseModel):
    """Model representing a car."""

    id: str
    car_model: str
    fuel_type: str
    consumption: float


class CarReport(BaseModel):
    """Model representing a car report for fuel consumption."""

    id: str
    car_model: str
    fuel_type: str
    mileage: float
    used_fuel: float


class Message(BaseModel):
    """Model for generic response messages."""

    message: str


# Predefined list of cars
cars = [
    Car(
        id="6137f257-a2d2-447d-9fbf-0122164b361b",
        car_model="Ford Raptor",
        fuel_type="gas",
        consumption=15.9,
    ),
    Car(
        id="c16beeec-0c5f-448c-94e2-98c007aa4734",
        car_model="Jeep Compass",
        fuel_type="gas",
        consumption=9.3,
    ),
    Car(
        id="b658bd54-7cbe-4342-aca3-b08bbf9f7f5d",
        car_model="Dacia Duster",
        fuel_type="gas",
        consumption=5.4,
    ),
    Car(
        id="a2577337-ba03-45be-8e66-d1d533cf0b8f",
        car_model="Citroen C3",
        fuel_type="gas",
        consumption=4.7,
    ),
    Car(
        id="3791a7ab-2c24-4675-a111-72693f2c4291",
        car_model="Fiat 500",
        fuel_type="gas",
        consumption=4.3,
    ),
    Car(
        id="58ee929f-815e-4a71-b568-85dc505a6f98",
        car_model="Ford Fiesta",
        fuel_type="gas",
        consumption=5.2,
    ),
    Car(
        id="d68c01a1-e1e1-4632-b832-b7852209864e",
        car_model="Hyundai i20",
        fuel_type="diesel",
        consumption=5.6,
    ),
    Car(
        id="793b849f-4a20-4851-9f2e-266db332818d",
        car_model="Opel Astra",
        fuel_type="diesel",
        consumption=5.3,
    ),
    Car(
        id="20b7de84-7df8-4455-b6f7-14a5b23db882",
        car_model="Peugeot 108",
        fuel_type="diesel",
        consumption=4.4,
    ),
    Car(
        id="c4ed6aa9-a507-48ba-9e7e-d471d621cdfa",
        car_model="Toyota Aygo",
        fuel_type="diesel",
        consumption=3.7,
    ),
    Car(
        id="5e3d4a33-bf69-48b7-ac1a-857416fd4977",
        car_model="Seat Ibiza",
        fuel_type="diesel",
        consumption=6.3,
    ),
    Car(
        id="77c85822-ec76-43f2-a40a-bd326cc85a0a",
        car_model="Alfa Romeo Giulia",
        fuel_type="diesel",
        consumption=6.7,
    ),
]


def get_car(car_id: str) -> Optional[Car]:
    """Retrieve a car by its ID."""
    for car in cars:
        if car_id == car.id:
            return car
    return None


def valid_car_report(car: Car, car_report: CarReport) -> bool:
    """
    Validate the car report based on fuel consumption.

    Args:
        car (Car): The car object.
        car_report (CarReport): The car report object.

    Returns:
        bool: True if the report is valid, False otherwise.
    """
    if car_report.mileage <= 0 or car_report.used_fuel <= 0:
        return False

    expected_used_fuel = car.consumption * (car_report.mileage / 100)
    return math.isclose(expected_used_fuel, car_report.used_fuel)


@app.post(
    "/api/v1/car-report", response_model=Message, responses={404: {"model": Message}}
)
async def submit_car_report(car_report: CarReport):
    """
    Submit a car report for validation.

    Args:
        car_report (CarReport): The car report to validate.

    Returns:
        JSONResponse: A response indicating the status of the report submission.
    """
    car = get_car(car_id=car_report.id)
    if not car:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "Car not found"}
        )

    is_valid = valid_car_report(car, car_report)
    logger.info(
        "car id: %s | car model: %s | fuel type: %s | mileage: %.2f - result: %s",
        car.id,
        car.car_model,
        car.fuel_type,
        car_report.mileage,
        "valid" if is_valid else "invalid",
    )

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={"message": "Car status report accepted"},
    )


@app.get("/healthz", status_code=status.HTTP_204_NO_CONTENT)
async def get_healthz():
    """
    Health check endpoint.

    Returns:
        Response: An HTTP 204 response indicating the service is up.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)
