from unittest.mock import MagicMock

import pytest

from flask_app.user.auth.exceptions import AuthenticationError, ValidationError
from flask_app.user.auth.services import AuthService
from flask_app.user.dtos import UserDTO
from flask_app.user.repositories import UserRepository


@pytest.fixture
def setup_repository():
    mock_session = MagicMock()
    user_repository = UserRepository(mock_session)
    return user_repository


@pytest.fixture
def setup_auth_service(setup_repository):
    email_service_mock = MagicMock()
    auth_service = AuthService(setup_repository, email_service_mock)
    return auth_service


def test_register_user_success(setup_auth_service):
    result = setup_auth_service.register_user(
        "test_user", "test@example.com", "Password123!"
    )
    assert result.username == "test_user"
    assert result.email == "test@example.com"


def test_register_user_invalid_email(setup_auth_service):
    with pytest.raises(ValidationError):
        setup_auth_service.register_user("test_user", "invalid_email", "Password123!")


def test_login_user_success(setup_auth_service):
    user = UserDTO(
        email="test@example.com",
        password_hash="hashed_password",
        is_active=True,
        is_verified=True,
    )
    setup_auth_service.user_repository.get_user_by_email = MagicMock(return_value=user)
    setup_auth_service.user_repository.reset_failed_login_attempts = MagicMock()
    setup_auth_service.user_repository.update_last_login = MagicMock()

    result = setup_auth_service.login_user("test@example.com", "Password123!")
    assert result.email == "test@example.com"


def test_login_user_invalid_credentials(setup_auth_service):
    setup_auth_service.user_repository.get_user_by_email = MagicMock(return_value=None)
    with pytest.raises(AuthenticationError):
        setup_auth_service.login_user("nonexistent@example.com", "Password123!")


def test_verify_email_success(setup_auth_service):
    user = UserDTO(email="test@example.com", verification_token="valid_token")
    setup_auth_service.user_repository.get_user_by_verification_token = MagicMock(
        return_value=user
    )

    result = setup_auth_service.verify_email("valid_token")
    assert result.is_verified is True


def test_verify_email_invalid_token(setup_auth_service):
    setup_auth_service.user_repository.get_user_by_verification_token = MagicMock(
        return_value=None
    )
    with pytest.raises(TokenInvalidError):
        setup_auth_service.verify_email("invalid_token")
