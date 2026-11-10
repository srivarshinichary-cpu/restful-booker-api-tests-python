import pytest

import config


@pytest.mark.smoke
@pytest.mark.regression
def test_valid_credentials_return_token(client):
    response = client.create_token(config.USERNAME, config.PASSWORD)

    assert response.status_code == 200
    assert response.json().get("token"), "token should be present and non-empty"


# Note: Restful-Booker returns HTTP 200 with a "reason" field for bad credentials (not 401).
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password",
    [
        ("admin", "wrongpassword"),
        ("wronguser", "password123"),
        ("", ""),
        ("admin", ""),
    ],
    ids=["wrong-password", "wrong-user", "both-empty", "empty-password"],
)
def test_invalid_credentials_are_rejected(client, username, password):
    response = client.create_token(username, password)

    assert response.status_code == 200
    body = response.json()
    assert body.get("reason") == "Bad credentials"
    assert "token" not in body
