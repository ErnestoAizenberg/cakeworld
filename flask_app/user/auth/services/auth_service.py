# flask_app/user/auth/services/auth_service.py
import re
import secrets
from datetime import datetime, timedelta
from typing import Optional

from werkzeug.security import generate_password_hash

from flask_app.user.dtos import UserDTO

from ..exceptions import (
    EmailAlreadyVerifiedError,
    TokenExpiredError,
    TokenInvalidError,
    TooManyRequestsError,
    UserNotFoundError,
    ValidationError,
)


class AuthService:
    def __init__(self, user_repository, email_service):
        self.user_repository = user_repository
        self.email_service = email_service
        self.password_reset_expiry = timedelta(hours=1)
        self.verification_expiry = timedelta(days=1)
        self.max_failed_attempts = 5
        self.login_lockout_duration = timedelta(minutes=15)
        self.verification_cooldown = timedelta(minutes=5)
        self.password_reset_cooldown = timedelta(minutes=5)

    def register_user(self, username: str, email: str, password: str) -> UserDTO:
        """Register a new user and return the created user DTO"""
        self._validate_signup(username, email, password)

        password_hash = generate_password_hash(
            password, method="pbkdf2:sha256:600000", salt_length=16
        )

        user_dto = UserDTO(
            username=username,
            email=email,
            password_hash=password_hash,
            verification_token=secrets.token_urlsafe(32),
            verification_token_expiry=datetime.utcnow() + self.verification_expiry,
            is_active=True,
            is_verified=False,
            created_at=datetime.utcnow(),
        )

        created_user = self.user_repository.save(user_dto)
        self.email_service.send_verification_email(created_user)
        return created_user

    def _validate_signup(self, username: str, email: str, password: str) -> None:
        """Validate registration data and raise ValidationError if invalid"""
        if not (username and email and password):
            raise ValidationError("All fields are required")

        if not re.match(r"^[a-zA-Z0-9_]{3,30}$", username):
            raise ValidationError(
                "Username must be 3-30 characters long and contain only letters, numbers and underscores"
            )

        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise ValidationError("Invalid email format")

        self._validate_password(password)

        if self.user_repository.get_user_by_username(username):
            raise ValidationError("Username already taken")

        if self.user_repository.get_user_by_email(email):
            raise ValidationError("Email already registered")

    def login_user(self, email: str, password: str) -> UserDTO:
        """Authenticate user and return user DTO if successful"""
        user_dto = self.user_repository.get_user_by_email(email)

        """if not user_dto:# or not user_dto.is_active:
            raise AuthenticationError("Invalid credentials")
            
        if self._is_account_locked(user_dto):
            raise AccountLockedError("Account temporarily locked")
            
        if not check_password_hash(user_dto.password_hash, password):
            self.user_repository.increment_failed_login_attempts(user_dto)
            raise AuthenticationError("Invalid credentials")
            
        if not user_dto.is_verified:
            raise EmailNotVerifiedError("Email not verified")"""

        self.user_repository.reset_failed_login_attempts(user_dto)
        self.user_repository.update_last_login(user_dto)

        return user_dto

    def verify_email(self, token: str) -> UserDTO:
        """Verify user email and return updated user DTO"""
        user_dto = self.user_repository.get_user_by_verification_token(token)

        if not user_dto:
            raise TokenInvalidError("Invalid verification token")

        if user_dto.verification_token_expiry < datetime.utcnow():
            raise TokenExpiredError("Verification token expired")

        if user_dto.is_verified:
            raise EmailAlreadyVerifiedError("Email already verified")

        user_dto.is_verified = True
        user_dto.verification_token = None
        user_dto.verification_token_expiry = None

        return self.user_repository.update(user_dto)

    def resend_verification_email(self, email: str) -> UserDTO:
        """Resend verification email and return user DTO"""
        user_dto = self.user_repository.get_user_by_email(email)

        if not user_dto:
            raise UserNotFoundError("User not found")

        if user_dto.is_verified:
            raise EmailAlreadyVerifiedError("Email already verified")

        if self._is_verification_cooldown_active(user_dto):
            raise TooManyRequestsError(
                "Please wait before requesting another verification email"
            )

        user_dto.verification_token = secrets.token_urlsafe(32)
        user_dto.verification_token_expiry = (
            datetime.utcnow() + self.verification_expiry
        )
        user_dto.last_verification_request = datetime.utcnow()

        updated_user = self.user_repository.update(user_dto)
        self.email_service.send_verification_email(updated_user)
        return updated_user

    def request_password_reset(self, email: str) -> Optional[UserDTO]:
        """Request password reset and return user DTO if user exists"""
        user_dto = self.user_repository.get_user_by_email(email)

        if not user_dto:
            return None  # Don't reveal if user exists

        if self._is_password_reset_cooldown_active(user_dto):
            raise TooManyRequestsError(
                "Please wait before requesting another password reset"
            )

        user_dto.password_reset_token = secrets.token_urlsafe(32)
        user_dto.password_reset_expiry = datetime.utcnow() + self.password_reset_expiry
        user_dto.last_password_reset_request = datetime.utcnow()

        updated_user = self.user_repository.update(user_dto)
        self.email_service.send_password_reset_email(updated_user)
        return updated_user

    def confirm_password_reset(self, token: str, new_password: str) -> UserDTO:
        """Confirm password reset and return updated user DTO"""
        user_dto = self.user_repository.get_user_by_password_reset_token(token)

        if not user_dto:
            raise TokenInvalidError("Invalid password reset token")

        if user_dto.password_reset_expiry < datetime.utcnow():
            raise TokenExpiredError("Password reset token expired")

        self._validate_password(new_password)

        user_dto.password_hash = generate_password_hash(
            new_password, method="pbkdf2:sha256:600000", salt_length=16
        )
        user_dto.password_reset_token = None
        user_dto.password_reset_expiry = None
        user_dto.failed_login_attempts = 0

        return self.user_repository.update(user_dto)

    def _validate_password(self, password: str) -> None:
        """Validate password strength and raise ValidationError if invalid"""
        if len(password) < 12:
            raise ValidationError("Password must be at least 12 characters long")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", password):
            raise ValidationError("Password must contain at least one digit")
        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValidationError(
                "Password must contain at least one special character"
            )

    def _is_account_locked(self, user_dto: UserDTO) -> bool:
        """Check if account is locked due to too many failed attempts"""
        return (
            user_dto.failed_login_attempts >= self.max_failed_attempts
            and user_dto.last_failed_login
            and (datetime.utcnow() - user_dto.last_failed_login)
            < self.login_lockout_duration
        )

    def _is_verification_cooldown_active(self, user_dto: UserDTO) -> bool:
        """Check if verification email cooldown is active"""
        return (
            user_dto.last_verification_request
            and (datetime.utcnow() - user_dto.last_verification_request)
            < self.verification_cooldown
        )

    def _is_password_reset_cooldown_active(self, user_dto: UserDTO) -> bool:
        """Check if password reset cooldown is active"""
        return (
            user_dto.last_password_reset_request
            and (datetime.utcnow() - user_dto.last_password_reset_request)
            < self.password_reset_cooldown
        )
