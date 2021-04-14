import json

import pytest
from fastapi import status
from starlette.testclient import TestClient

from ..app.utils import token
from ..app.utils.http import HTTPFactory


@pytest.mark.parametrize(
    "payload, credential_status_code, status_code",
    [
        [{"username": "some_existing_user", "password": "some_existing_password"}, status.HTTP_200_OK, status.HTTP_200_OK],
        [{"username": "some_existing_user", "password": "not_corresponding_password"}, status.HTTP_401_UNAUTHORIZED,
         status.HTTP_401_UNAUTHORIZED],
    ]
)
def test_check_credentials(test_app: TestClient, monkeypatch, payload, credential_status_code, status_code):
    async def mock_check_user_credentials(user):
        if credential_status_code == status.HTTP_200_OK:
            return {"username": payload["username"], "id": 1}
        if credential_status_code == status.HTTP_401_UNAUTHORIZED:
            return {"detail": "Incorrect username or password"}

    monkeypatch.setattr(HTTPFactory, "check_user_credentials", mock_check_user_credentials)
    response = test_app.post("/auth/login", data=json.dumps(payload))
    assert response.status_code == status_code


def test_verify_token(test_app: TestClient):
    access_token = token.create_access_token(data={"username": "some_username", "id": 1})
    test_app.headers["access-token"] = access_token
    response = test_app.post("/auth/credentials")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "some_username"
    assert response.json()["user_id"] == 1
