# flask_app/user/auth/controllers.py
import logging
from functools import wraps

from flask_app.user.dtos import UserDTO

from .exceptions import AuthException, ValidationError
from .services.auth_service import AuthService

logger = logging.getLogger(__name__)


def handle_auth_errors(f):
    """Decorator to handle authentication-related exceptions."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            logger.warning(f"Validation error: {str(e)}")
            raise AuthException(str(e), 400)
        except AuthException as e:
            logger.warning(f"Auth error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            raise AuthException("An unexpected error occurred", 500)

    return wrapper


class AuthController:
    """Manage servuces needed for authentication process."""

    def __init__(self, auth_service: AuthService, notification_service):
        self.auth_service = auth_service
        self.notification_service = notification_service

    @handle_auth_errors
    def register(
        self, username: str, email: str, password: str, confirm_password: str
    ) -> UserDTO:
        """Register a new user account.

        Args:
            username: User's display name
            email: User's email address
            password: User's password
            confirm_password: Password confirmation

        Returns:
            UserDTO: Registered user data

        Raises:
            AuthException: If registration fails
            ValidationError: If input validation fails
        """
        if password != confirm_password:
            raise ValidationError("Passwords do not match")

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")

        return self.auth_service.register_user(username, email, password)

    @handle_auth_errors
    def login(self, email: str, password: str) -> UserDTO:
        """Authenticate a user.

        Args:
            email: User's email address
            password: User's password

        Returns:
            UserDTO: Authenticated user data

        Raises:
            AuthException: If authentication fails
        """
        user = self.auth_service.login_user(email, password)
        return user

    @handle_auth_errors
    def verify_email(self, token: str) -> bool:
        """Verify a user's email address using verification token.

        Args:
            token: Email verification token

        Returns:
            bool: True if verification succeeded

        Raises:
            AuthException: If verification fails
        """
        return self.auth_service.verify_email(token)

    @handle_auth_errors
    def resend_verification(self, email: str) -> bool:
        """Resend email verification link.

        Args:
            email: User's email address

        Returns:
            bool: True if email was sent

        Raises:
            AuthException: If operation fails
        """
        return self.auth_service.resend_verification_email(email)

    @handle_auth_errors
    def request_password_reset(self, email: str) -> bool:
        """Request a password reset email.

        Args:
            email: User's email address

        Returns:
            bool: True if request was processed

        Raises:
            AuthException: If operation fails
        """
        return self.auth_service.request_password_reset(email)

    @handle_auth_errors
    def reset_password(
        self, token: str, new_password: str, confirm_password: str
    ) -> bool:
        """Reset user's password using reset token.

        Args:
            token: Password reset token
            new_password: New password
            confirm_password: Password confirmation

        Returns:
            bool: True if password was reset

        Raises:
            AuthException: If operation fails
            ValidationError: If input validation fails
        """
        if new_password != confirm_password:
            raise ValidationError("Passwords do not match")

        if len(new_password) < 8:
            raise ValidationError("Password must be at least 8 characters")

        return self.auth_service.confirm_password_reset(token, new_password)

    def send_welcome_notification(
        self,
        user: "UserDTO",
        message: str,
        type: str = "info",
    ):
        print(f"Sending {type} notification to {user.username}: {message}")
        self.notification_service.add_notification(
            user.id,
            message,
            type=type,
        )
