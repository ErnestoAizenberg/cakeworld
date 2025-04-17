from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest
from werkzeug.security import generate_password_hash

from flask_app.user.auth.services import AuthService
from flask_app.user.dtos import UserDTO


class TestAuthService:
    """Comprehensive test suite for AuthService"""

    @pytest.fixture
    def auth_service(self):
        """Fixture providing configured AuthService instance"""
        user_service = Mock()
        email_service = Mock()
        return AuthService(user_service, email_service)

    @pytest.fixture
    def valid_user_dto(self):
        """Fixture providing a valid UserDTO instance"""
        return UserDTO(
            id=1,
            email="test@example.com",
            password_hash=generate_password_hash("ValidPass123!"),
            is_active=True,
            is_verified=True,
            failed_login_attempts=0,
            last_failed_login=None,
        )

    def test_login_user_success(self, auth_service, valid_user_dto):
        """Test successful user login scenario"""
        # Setup
        auth_service.user_service.get_user_by_email.return_value = valid_user_dto
        auth_service.user_service.check_password_hash = (
            lambda h, p: check_password_hash(h, p)
        )

        # Execute
        result = auth_service.login_user("test@example.com", "ValidPass123!")

        # Verify
        assert result["success"] == "Logged in successfully"
        assert result["user_id"] == 1
        auth_service.user_service.reset_failed_login_attempts.assert_called_once_with(
            valid_user_dto
        )
        auth_service.user_service.update_last_login.assert_called_once_with(
            valid_user_dto
        )

    def test_login_user_inactive(self, auth_service, valid_user_dto):
        """Test login attempt with inactive account"""
        # Setup
        valid_user_dto.is_active = False
        auth_service.user_service.get_user_by_email.return_value = valid_user_dto

        # Execute
        result = auth_service.login_user("test@example.com", "ValidPass123!")

        # Verify
        assert result["error"] == "Invalid email or password"
        auth_service.user_service.reset_failed_login_attempts.assert_not_called()

    def test_login_user_wrong_password(self, auth_service, valid_user_dto):
        """Test login attempt with wrong password"""
        # Setup
        auth_service.user_service.get_user_by_email.return_value = valid_user_dto
        auth_service.user_service.check_password_hash = lambda h, p: False

        # Execute
        result = auth_service.login_user("test@example.com", "WrongPass123!")

        # Verify
        assert result["error"] == "Invalid email or password"
        auth_service.user_service.increment_failed_login_attempts.assert_called_once_with(
            valid_user_dto
        )

    def test_login_user_locked_account(self, auth_service, valid_user_dto):
        """Test login attempt with locked account"""
        # Setup
        valid_user_dto.failed_login_attempts = 5
        valid_user_dto.last_failed_login = datetime.utcnow() - timedelta(minutes=10)
        auth_service.user_service.get_user_by_email.return_value = valid_user_dto

        # Execute
        result = auth_service.login_user("test@example.com", "ValidPass123!")

        # Verify
        assert (
            result["error"]
            == "Account temporarily locked due to too many failed attempts. Try again later."
        )

    def test_login_user_unverified(self, auth_service, valid_user_dto):
        """Test login attempt with unverified email"""
        # Setup
        valid_user_dto.is_verified = False
        auth_service.user_service.get_user_by_email.return_value = valid_user_dto
        auth_service.user_service.check_password_hash = (
            lambda h, p: check_password_hash(h, p)
        )

        # Execute
        result = auth_service.login_user("test@example.com", "ValidPass123!")

        # Verify
        assert result["error"] == "Please verify your email before logging in."

    def test_register_user_success(self, auth_service):
        """Test successful user registration"""
        # Setup
        auth_service.user_service.get_user_by_username.return_value = None
        auth_service.user_service.get_user_by_email.return_value = None
        auth_service.user_service.create_user.return_value = UserDTO(id=1)

        # Execute
        result = auth_service.register_user(
            "newuser", "new@example.com", "ValidPassword123!"
        )

        # Verify
        assert (
            result["success"]
            == "Registration successful! Please check your email to verify your account."
        )
        auth_service.email_service.send_verification_email.assert_called_once()

    @pytest.mark.parametrize(
        "username,email,password,expected_error",
        [
            ("", "test@example.com", "password", "All fields are required."),
            ("test", "", "password", "All fields are required."),
            ("test", "test@example.com", "", "All fields are required."),
            (
                "te",
                "test@example.com",
                "password",
                "Username must be 3-30 characters long",
            ),
            (
                "test@user",
                "test@example.com",
                "password",
                "Username must be 3-30 characters long",
            ),
            ("testuser", "invalid-email", "password", "Invalid email format"),
            (
                "testuser",
                "test@example.com",
                "short",
                "Password must be at least 12 characters long",
            ),
            (
                "testuser",
                "test@example.com",
                "nouppercase123!",
                "Password must contain at least one uppercase letter",
            ),
            (
                "testuser",
                "test@example.com",
                "NOLOWERCASE123!",
                "Password must contain at least one lowercase letter",
            ),
            (
                "testuser",
                "test@example.com",
                "NoDigits!",
                "Password must contain at least one digit",
            ),
            (
                "testuser",
                "test@example.com",
                "NoSpecialChars123",
                "Password must contain at least one special character",
            ),
        ],
    )
    def test_register_user_validation(
        self, auth_service, username, email, password, expected_error
    ):
        """Test user registration validation"""
        # Setup
        auth_service.user_service.get_user_by_username.return_value = None
        auth_service.user_service.get_user_by_email.return_value = None

        # Execute
        result = auth_service.register_user(username, email, password)

        # Verify
        assert result["error"].startswith(expected_error)

    def test_verify_email_success(self, auth_service, valid_user_dto):
        """Test successful email verification"""
        # Setup
        valid_user_dto.is_verified = False
        valid_user_dto.verification_token = "valid_token"
        valid_user_dto.verification_token_expiry = datetime.utcnow() + timedelta(
            hours=1
        )
        auth_service.user_service.get_user_by_verification_token.return_value = (
            valid_user_dto
        )

        # Execute
        result = auth_service.verify_email("valid_token")

        # Verify
        assert result["success"] == "Email verification successful! You can now log in."
        assert valid_user_dto.is_verified is True
        auth_service.user_service.update_user.assert_called_once_with(valid_user_dto)

    def test_verify_email_expired(self, auth_service, valid_user_dto):
        """Test expired verification token"""
        # Setup
        valid_user_dto.verification_token_expiry = datetime.utcnow() - timedelta(
            hours=1
        )
        auth_service.user_service.get_user_by_verification_token.return_value = (
            valid_user_dto
        )

        # Execute
        result = auth_service.verify_email("expired_token")

        # Verify
        assert (
            result["error"]
            == "Verification link has expired. Please request a new one."
        )

    def test_resend_verification_email_success(self, auth_service, valid_user_dto):
        """Test successful verification email resend"""
        # Setup
        valid_user_dto.is_verified = False
        auth_service.user_service.get_user_by_email.return_value = valid_user_dto

        # Execute
        result = auth_service.resend_verification_email("test@example.com")

        # Verify
        assert (
            result["success"]
            == "A new verification link has been sent to your email address."
        )
        assert valid_user_dto.verification_token is not None
        auth_service.email_service.send_verification_email.assert_called_once()

    def test_request_password_reset_success(self, auth_service, valid_user_dto):
        """Test successful password reset request"""
        # Setup
        auth_service.user_service.get_user_by_email.return_value = valid_user_dto

        # Execute
        result = auth_service.request_password_reset("test@example.com")

        # Verify
        assert (
            result["success"]
            == "A password reset link has been sent to your email address."
        )
        assert valid_user_dto.password_reset_token is not None
        auth_service.email_service.send_password_reset_email.assert_called_once()

    def test_confirm_password_reset_success(self, auth_service, valid_user_dto):
        """Test successful password reset confirmation"""
        # Setup
        valid_user_dto.password_reset_token = "valid_token"
        valid_user_dto.password_reset_expiry = datetime.utcnow() + timedelta(hours=1)
        auth_service.user_service.get_user_by_password_reset_token.return_value = (
            valid_user_dto
        )

        # Execute
        result = auth_service.confirm_password_reset("valid_token", "NewValidPass123!")

        # Verify
        assert result["success"] == "Your password has been reset successfully."
        assert valid_user_dto.password_reset_token is None
        auth_service.user_service.update_user.assert_called_once_with(valid_user_dto)
