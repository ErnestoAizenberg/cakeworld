import re
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional

from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app

from flask_app.user.dtos import UserDTO


class AuthService:
    def __init__(self, user_service, email_service):
        self.user_service = user_service
        self.email_service = email_service
        self.password_reset_expiry = timedelta(hours=1)
        self.verification_expiry = timedelta(days=1)

    def register_user(self, username: str, email: str, password: str) -> Dict:
        """Регистрирует нового пользователя."""
        validation_error = self._validate_signup(username, email, password)
        if validation_error:
            return {"error": validation_error}

        # Хеширование пароля с усиленным алгоритмом
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
            last_login=None,
            failed_login_attempts=0,
        )

        try:
            self.user_service.create_user(user_dto)
            self.email_service.send_verification_email(user_dto)
            return {
                "success": "Registration successful! Please check your email to verify your account."
            }
        except Exception as e:
            current_app.logger.error(f"User registration failed: {str(e)}")
            return {
                "error": "Registration failed due to a server error. Please try again later."
            }

    def _validate_signup(
        self, username: str, email: str, password: str
    ) -> Optional[str]:
        """Валидация данных регистрации."""
        if not (username and email and password):
            return "All fields are required."

        if not re.match(r"^[a-zA-Z0-9_]{3,30}$", username):
            return "Username must be 3-30 characters long and contain only letters, numbers and underscores."

        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return "Invalid email format."

        if len(password) < 12:
            return "Password must be at least 12 characters long."
        if not re.search(r"[A-Z]", password):
            return "Password must contain at least one uppercase letter."
        if not re.search(r"[a-z]", password):
            return "Password must contain at least one lowercase letter."
        if not re.search(r"[0-9]", password):
            return "Password must contain at least one digit."
        if not re.search(r"[^A-Za-z0-9]", password):
            return "Password must contain at least one special character."

        if self.user_service.get_user_by_username(username):
            return "Username already taken."

        if self.user_service.get_user_by_email(email):
            return "Email already registered."

        return None

    def login_user(self, email: str, password: str) -> Dict:
        """Аутентифицирует пользователя."""
        user_dto = self.user_service.get_user_by_email(email)

        if not user_dto or not user_dto.is_active:
            return {"error": "Invalid email or password"}

        # Проверка блокировки из-за слишком многих попыток
        if (
            user_dto.failed_login_attempts >= 5
            and user_dto.last_failed_login
            and (datetime.utcnow() - user_dto.last_failed_login) < timedelta(minutes=15)
        ):
            return {
                "error": "Account temporarily locked due to too many failed attempts. Try again later."
            }

        if not check_password_hash(user_dto.password_hash, password):
            # Обновляем счетчик неудачных попыток
            self.user_service.increment_failed_login_attempts(user_dto)
            return {"error": "Invalid email or password"}

        if not user_dto.is_verified:
            return {"error": "Please verify your email before logging in."}

        # Сброс счетчика неудачных попыток при успешном входе
        self.user_service.reset_failed_login_attempts(user_dto)

        # Обновляем время последнего входа
        self.user_service.update_last_login(user_dto)

        return {"success": "Logged in successfully", "user_id": user_dto.id}

    def verify_email(self, token: str) -> Dict:
        """Подтверждает email пользователя."""
        user_dto = self.user_service.get_user_by_verification_token(token)

        if not user_dto:
            return {"error": "Invalid or expired verification link."}

        if user_dto.verification_token_expiry < datetime.utcnow():
            return {"error": "Verification link has expired. Please request a new one."}

        if user_dto.is_verified:
            return {"error": "Email is already verified."}

        try:
            user_dto.is_verified = True
            user_dto.verification_token = None
            user_dto.verification_token_expiry = None
            self.user_service.update_user(user_dto)
            return {"success": "Email verification successful! You can now log in."}
        except Exception as e:
            current_app.logger.error(f"Email verification failed: {str(e)}")
            return {"error": "Email verification failed. Please try again."}

    def resend_verification_email(self, email: str) -> Dict:
        """Отправляет повторное письмо для подтверждения email."""
        user_dto = self.user_service.get_user_by_email(email)

        if not user_dto:
            return {"error": "No user found with this email address."}

        if user_dto.is_verified:
            return {"error": "Your email is already verified."}

        # Проверяем частоту запросов
        if user_dto.last_verification_request and (
            datetime.utcnow() - user_dto.last_verification_request
        ) < timedelta(minutes=5):
            return {
                "error": "Please wait before requesting another verification email."
            }

        try:
            user_dto.verification_token = secrets.token_urlsafe(32)
            user_dto.verification_token_expiry = (
                datetime.utcnow() + self.verification_expiry
            )
            user_dto.last_verification_request = datetime.utcnow()
            self.user_service.update_user(user_dto)
            self.email_service.send_verification_email(user_dto)
            return {
                "success": "A new verification link has been sent to your email address."
            }
        except Exception as e:
            current_app.logger.error(f"Failed to resend verification email: {str(e)}")
            return {
                "error": "Failed to resend verification email. Please try again later."
            }

    def request_password_reset(self, email: str) -> Dict:
        """Обрабатывает запрос на сброс пароля."""
        user_dto = self.user_service.get_user_by_email(email)

        if not user_dto:
            # Не раскрываем информацию о существовании пользователя
            return {
                "success": "If an account exists with this email, a password reset link has been sent."
            }

        # Проверяем частоту запросов
        if user_dto.last_password_reset_request and (
            datetime.utcnow() - user_dto.last_password_reset_request
        ) < timedelta(minutes=5):
            return {"error": "Please wait before requesting another password reset."}

        try:
            user_dto.password_reset_token = secrets.token_urlsafe(32)
            user_dto.password_reset_expiry = (
                datetime.utcnow() + self.password_reset_expiry
            )
            user_dto.last_password_reset_request = datetime.utcnow()
            self.user_service.update_user(user_dto)
            self.email_service.send_password_reset_email(user_dto)
            return {
                "success": "A password reset link has been sent to your email address."
            }
        except Exception as e:
            current_app.logger.error(f"Password reset request failed: {str(e)}")
            return {
                "error": "Failed to process password reset request. Please try again later."
            }

    def confirm_password_reset(self, token: str, new_password: str) -> Dict:
        """Подтверждает сброс пароля."""
        user_dto = self.user_service.get_user_by_password_reset_token(token)

        if not user_dto:
            return {"error": "Invalid or expired password reset link."}

        if user_dto.password_reset_expiry < datetime.utcnow():
            return {
                "error": "Password reset link has expired. Please request a new one."
            }

        # Валидация нового пароля
        password_error = self._validate_password(new_password)
        if password_error:
            return {"error": password_error}

        try:
            # Хеширование нового пароля
            user_dto.password_hash = generate_password_hash(
                new_password, method="pbkdf2:sha256:600000", salt_length=16
            )
            user_dto.password_reset_token = None
            user_dto.password_reset_expiry = None
            user_dto.failed_login_attempts = 0  # Сброс счетчика неудачных попыток
            self.user_service.update_user(user_dto)
            return {
                "success": "Your password has been reset successfully. You can now log in with your new password."
            }
        except Exception as e:
            current_app.logger.error(f"Password reset failed: {str(e)}")
            return {"error": "Failed to reset password. Please try again later."}

    def _validate_password(self, password: str) -> Optional[str]:
        """Валидация пароля."""
        if len(password) < 12:
            return "Password must be at least 12 characters long."
        if not re.search(r"[A-Z]", password):
            return "Password must contain at least one uppercase letter."
        if not re.search(r"[a-z]", password):
            return "Password must contain at least one lowercase letter."
        if not re.search(r"[0-9]", password):
            return "Password must contain at least one digit."
        if not re.search(r"[^A-Za-z0-9]", password):
            return "Password must contain at least one special character."
        return None
