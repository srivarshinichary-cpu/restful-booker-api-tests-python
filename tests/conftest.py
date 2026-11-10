import pytest

import config
from clients.booking_client import BookingClient
from utils.data_builder import build_booking


@pytest.fixture(scope="session")
def client() -> BookingClient:
    return BookingClient()


@pytest.fixture(scope="session")
def token(client) -> str:
    response = client.create_token(config.USERNAME, config.PASSWORD)
    assert response.status_code == 200, f"Auth failed: {response.text}"
    return response.json()["token"]


@pytest.fixture
def new_booking(client, token):
    """Creates a booking for the test, then cleans it up afterwards."""
    payload = build_booking()
    response = client.create_booking(payload)
    assert response.status_code == 200, f"Setup failed: {response.text}"
    booking_id = response.json()["bookingid"]
    yield {"id": booking_id, "payload": payload}
    client.delete_booking(booking_id, token)  # best-effort cleanup
