from unittest.mock import MagicMock, patch

import pytest

from flask_app.user.auth.controllers import AuthController
from flask_app.user.auth.exceptions import AuthException, ValidationError
from flask_app.user.dtos import UserDTO


@pytest.fixture
def mock_auth_service():
    return MagicMock()


@pytest.fixture
def auth_controller(mock_auth_service):
    return AuthController(mock_auth_service)


class TestAuthController:
    """Test cases for AuthController."""

    def test_register_success(self, auth_controller, mock_auth_service):
        """Test successful user registration."""
        mock_user = UserDTO(id=1, username="test", email="test@example.com")
        mock_auth_service.register_user.return_value = mock_user

        result = auth_controller.register(
            "test", "test@example.com", "password123", "password123"
        )

        assert result == mock_user
        mock_auth_service.register_user.assert_called_once_with(
            "test", "test@example.com", "password123"
        )

    def test_register_password_mismatch(self, auth_controller):
        """Test registration with password mismatch."""
        with pytest.raises(ValidationError):
            auth_controller.register(
                "test", "test@example.com", "password123", "different"
            )

    def test_login_success(self, auth_controller, mock_auth_service):
        """Test successful login."""
        mock_user = UserDTO(id=1, username="test", email="test@example.com")
        mock_auth_service.login_user.return_value = mock_user

        result = auth_controller.login("test@example.com", "password123")

        assert result == mock_user

    def test_verify_email_success(self, auth_controller, mock_auth_service):
        """Test successful email verification."""
        mock_auth_service.verify_email.return_value = True

        result = auth_controller.verify_email("valid_token")

        assert result is True
        mock_auth_service.verify_email.assert_called_once_with("valid_token")

    def test_resend_verification_success(self, auth_controller, mock_auth_service):
        """Test successful verification email resend."""
        mock_auth_service.resend_verification_email.return_value = True

        result = auth_controller.resend_verification("test@example.com")

        assert result is True
        mock_auth_service.resend_verification_email.assert_called_once_with(
            "test@example.com"
        )

    def test_request_password_reset_success(self, auth_controller, mock_auth_service):
        """Test successful password reset request."""
        mock_auth_service.request_password_reset.return_value = True

        result = auth_controller.request_password_reset("test@example.com")

        assert result is True
        mock_auth_service.request_password_reset.assert_called_once_with(
            "test@example.com"
        )

    def test_reset_password_success(self, auth_controller, mock_auth_service):
        """Test successful password reset."""
        mock_auth_service.confirm_password_reset.return_value = True

        result = auth_controller.reset_password(
            "valid_token", "newpassword123", "newpassword123"
        )

        assert result is True
        mock_auth_service.confirm_password_reset.assert_called_once_with(
            "valid_token", "newpassword123"
        )
