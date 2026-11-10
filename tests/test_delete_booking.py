import pytest

from utils.data_builder import build_booking


# Note: Restful-Booker returns 201 Created for a successful delete (a known quirk).
@pytest.mark.smoke
@pytest.mark.regression
def test_delete_removes_booking(client, token):
    booking_id = client.create_booking(build_booking()).json()["bookingid"]

    delete_response = client.delete_booking(booking_id, token)

    assert delete_response.status_code == 201
    assert client.get_booking(booking_id).status_code == 404


@pytest.mark.negative
@pytest.mark.regression
def test_delete_without_token_is_forbidden_and_booking_remains(client, new_booking):
    response = client.delete_booking(new_booking["id"], token=None)

    assert response.status_code == 403
    assert client.get_booking(new_booking["id"]).status_code == 200


@pytest.mark.negative
@pytest.mark.regression
def test_delete_non_existent_booking_does_not_succeed(client, token):
    response = client.delete_booking(999999999, token)

    assert response.status_code in (404, 405)
