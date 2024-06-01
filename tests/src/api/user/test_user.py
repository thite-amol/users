"""Module to test users API."""

import json
from unittest.mock import AsyncMock

from src.config import settings


def test_register(mocker, client, admin_user):
    """Test user registration."""
    data = {
        "email": "user@example.com",
        "username": "username",
        "password": "abcd1234",
        "first_name": "User",
        "last_name": "Name",
    }

    payload = json.dumps(data)
    headers = {"Content-Type": "application/json"}

    async_mock = AsyncMock(return_value=None)
    mocker.patch(
        "src.users.service.UsersCRUD.get_by_username", side_effect=async_mock
    )
    mocker.patch(
        "src.users.service.UsersCRUD.get_user_by_email", side_effect=async_mock
    )
    mocker.patch(
        "src.users.service.UsersCRUD.create",
        side_effect=AsyncMock(return_value=admin_user),
    )

    response = client.post(
        f"{settings.API_V1_STR}/register", data=payload, headers=headers
    )

    data = response.json()
    assert data["code"] == 200
    assert "created_time" in data["data"]
    assert "password" in data["data"]
