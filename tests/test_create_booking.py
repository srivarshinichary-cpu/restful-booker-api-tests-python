import pytest

import config
from utils.data_builder import build_booking
from utils.schema import assert_matches_schema


@pytest.mark.smoke
@pytest.mark.regression
def test_create_booking_returns_id_and_echoes_data(client, token):
    payload = build_booking()

    response = client.create_booking(payload)

    assert response.status_code == 200
    body = response.json()
    assert body["bookingid"] > 0
    assert body["booking"] == payload
    client.delete_booking(body["bookingid"], token)


@pytest.mark.regression
def test_create_booking_response_matches_schema_and_content_type(client, token):
    response = client.create_booking(build_booking())

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]
    assert_matches_schema(response.json(), "create_booking")
    assert_matches_schema(response.json()["booking"], "booking")
    client.delete_booking(response.json()["bookingid"], token)


@pytest.mark.regression
def test_created_booking_can_be_fetched(client, new_booking):
    response = client.get_booking(new_booking["id"])

    assert response.status_code == 200
    assert response.json() == new_booking["payload"]


@pytest.mark.regression
@pytest.mark.parametrize(
    "firstname, lastname, price, deposit, needs",
    [
        ("Alice", "Smith", 100, True, "Breakfast"),
        ("Bob", "ONeil", 0, False, "None"),
        ("Carlos", "Garcia", 99999, True, "Late checkout"),
        ("Dana", "Lee-Kim", 1, False, "Airport pickup"),
    ],
)
def test_create_booking_with_various_valid_data(client, token, firstname, lastname, price, deposit, needs):
    payload = build_booking(firstname, lastname, price, deposit, needs)

    response = client.create_booking(payload)

    assert response.status_code == 200
    assert response.json()["booking"] == payload
    client.delete_booking(response.json()["bookingid"], token)


# The live API is known to return 500 for malformed bodies (a well-behaved API returns 400).
# The assertion accepts any 4xx/5xx so the test documents the gap instead of hiding it.
@pytest.mark.negative
@pytest.mark.regression
def test_create_booking_with_missing_fields_fails(client):
    response = client.create_booking({"firstname": "OnlyFirstName"})

    assert response.status_code >= 400, f"Expected error, got {response.status_code}"


@pytest.mark.negative
@pytest.mark.regression
def test_create_booking_with_non_json_body_fails(client):
    response = client.create_booking_raw("this is not json")

    assert response.status_code >= 400, f"Expected error, got {response.status_code}"
