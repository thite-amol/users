"""Module to test auth API."""

import json
from unittest.mock import AsyncMock

import pytest

from src.common.exception import errors
from src.config import settings

PYTEST_USERNAME = "admin"
PYTEST_PASSWORD = "string"


def test_login(mocker, client, admin_user, user_repo) -> None:
    """Test normal user login."""
    data = {
        "username": PYTEST_USERNAME,
        "password": PYTEST_PASSWORD,
    }

    payload = json.dumps(data)
    headers = {"Content-Type": "application/json"}

    async_mock = AsyncMock(return_value=admin_user)
    mocker.patch(
        "src.auth.service.UsersCRUD.get_by_username", side_effect=async_mock
    )
    mocker.patch(
        "src.auth.service.UsersCRUD.update_login_time", return_value=True
    )
    response = client.post(
        f"{settings.API_V1_STR}/login", data=payload, headers=headers
    )

    data = response.json()
    assert data["code"] == 200
    assert "access_token" in data["data"]
    assert "token_type" in data["data"]


def test_login_user_not_exist(mocker, client, admin_user):
    """Test login if user not exist."""
    data = {
        "username": PYTEST_USERNAME,
        "password": PYTEST_PASSWORD,
    }

    payload = json.dumps(data)
    headers = {"Content-Type": "application/json", "accept": "application/json"}

    async_mock = AsyncMock(return_value=False)
    mocker.patch(
        "src.auth.service.UsersCRUD.get_by_username", side_effect=async_mock
    )

    with pytest.raises(errors.NotFoundError):  # noqa: PT011
        client.post(
            f"{settings.API_V1_STR}/login", data=payload, headers=headers
        )
