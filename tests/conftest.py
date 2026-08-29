import pytest
from src.clients.booker_client import BookerClient


@pytest.fixture(scope="session")
def client():
    c = BookerClient()
    c.login()
    return c


@pytest.fixture
def sample_booking():
    return {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-01-01",
            "checkout": "2024-01-02"
        },
        "additionalneeds": "Breakfast"
    }