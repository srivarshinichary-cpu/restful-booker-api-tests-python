import pytest

import config
from utils.schema import assert_matches_schema


@pytest.mark.smoke
@pytest.mark.regression
def test_get_all_booking_ids(client):
    response = client.get_booking_ids()

    assert response.status_code == 200
    ids = response.json()
    assert len(ids) > 0
    assert all("bookingid" in item for item in ids)


@pytest.mark.regression
def test_get_booking_by_id_matches_schema(client, new_booking):
    response = client.get_booking(new_booking["id"])

    assert response.status_code == 200
    assert_matches_schema(response.json(), "booking")


@pytest.mark.negative
@pytest.mark.regression
def test_get_non_existent_booking_returns_404(client):
    response = client.get_booking(999999999)

    assert response.status_code == 404


@pytest.mark.regression
def test_filter_bookings_by_name(client, new_booking):
    payload = new_booking["payload"]

    response = client.get_booking_ids(firstname=payload["firstname"], lastname=payload["lastname"])

    assert response.status_code == 200
    assert new_booking["id"] in [item["bookingid"] for item in response.json()]


@pytest.mark.regression
def test_response_time_under_threshold(client):
    response = client.get_booking_ids()

    elapsed_ms = response.elapsed.total_seconds() * 1000
    assert response.status_code == 200
    assert elapsed_ms < config.MAX_RESPONSE_TIME_MS, f"Took {elapsed_ms:.0f} ms"


@pytest.mark.regression
def test_response_headers_are_present(client):
    response = client.get_booking_ids()

    assert response.status_code == 200
    assert "Content-Type" in response.headers
    assert "Server" in response.headers
