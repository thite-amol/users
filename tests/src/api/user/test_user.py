"""Module to test users API."""

import json
from unittest.mock import AsyncMock

import pytest

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
        f"{settings.base.API_V1_STR}/register", data=payload, headers=headers
    )

    data = response.json()
    assert data["code"] == 200
    assert "created_time" in data["data"]
    assert "password" in data["data"]


def test_register_missing_data(mocker, client, admin_user):
    """Test user registration with missing data."""
    data = {
        "email": "user@example.com",
        "username": "username",
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
        f"{settings.base.API_V1_STR}/register", data=payload, headers=headers
    )

    data = response.json()
    assert data["code"] == 422
    assert data["msg"] == "Invalid request data. Please provide correct inputs."


@pytest.mark.parametrize(
    ("email_exist", "username_exist", "expected_message"),
    [
        pytest.param(True, False, "The email has been registered"),
        pytest.param(False, True, "This username is already registered"),
    ],
)
def test_register_with_existing_user(
    mocker, client, admin_user, email_exist, username_exist, expected_message
):
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

    async_mock = AsyncMock(return_value=admin_user if username_exist else None)
    mocker.patch(
        "src.users.service.UsersCRUD.get_by_username", side_effect=async_mock
    )

    async_mock = AsyncMock(return_value=admin_user if email_exist else None)
    mocker.patch(
        "src.users.service.UsersCRUD.get_user_by_email", side_effect=async_mock
    )
    mocker.patch(
        "src.users.service.UsersCRUD.create",
        side_effect=AsyncMock(return_value=admin_user),
    )

    response = client.post(
        f"{settings.base.API_V1_STR}/register", data=payload, headers=headers
    )

    data = response.json()
    assert data["code"] == 400
    assert data["msg"] == expected_message
