import pytest

from utils.data_builder import build_booking


@pytest.mark.smoke
@pytest.mark.regression
def test_put_updates_all_fields(client, token, new_booking):
    updated = build_booking("UpdatedFirst", "UpdatedLast", 777, False, "Dinner")

    response = client.update_booking(new_booking["id"], updated, token)

    assert response.status_code == 200
    assert response.json() == updated


@pytest.mark.negative
@pytest.mark.regression
def test_put_without_token_is_forbidden(client, new_booking):
    response = client.update_booking(new_booking["id"], build_booking(), token=None)

    assert response.status_code == 403


@pytest.mark.negative
@pytest.mark.regression
def test_put_with_invalid_token_is_forbidden(client, new_booking):
    response = client.update_booking(new_booking["id"], build_booking(), token="invalid-token")

    assert response.status_code == 403


@pytest.mark.regression
def test_patch_updates_only_supplied_fields(client, token, new_booking):
    original = new_booking["payload"]

    response = client.partial_update_booking(new_booking["id"], {"firstname": "PatchedName"}, token)

    assert response.status_code == 200
    body = response.json()
    assert body["firstname"] == "PatchedName"
    assert body["lastname"] == original["lastname"], "lastname must be unchanged"
    assert body["totalprice"] == original["totalprice"], "totalprice must be unchanged"


@pytest.mark.negative
@pytest.mark.regression
def test_patch_without_token_is_forbidden(client, new_booking):
    response = client.partial_update_booking(new_booking["id"], {"firstname": "Nope"}, token=None)

    assert response.status_code == 403
