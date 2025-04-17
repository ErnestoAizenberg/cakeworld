import secrets
from datetime import datetime, timedelta

from flask import flash

from .dtos import UserDTO


class AuthService:
    def __init__(self, user_service):
        self.user_service = user_service

    def signup(self, username: str, email: str, password: str) -> str:
        validation_error = self._validate_signup(username, email, password)
        if validation_error:
            return validation_error

        user_dto = UserDTO(
            username=username,
            email=email,
            password_hash=self.user_service.hash_password(password),
            verification_token=secrets.token_urlsafe(32),
        )
        self.user_service.create_user(user_dto)

        self._send_verification_email(user_dto)
        return (
            "Registration successful! Please check your email to verify your account."
        )

    def _validate_signup(self, username: str, email: str, password: str) -> str:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Invalid email format."

        if (
            len(password) < 8
            or not re.search(r"\d", password)
            or not re.search(r"[A-Za-z]", password)
        ):
            return "Password must be at least 8 characters long and include both letters and numbers."

        if self.user_service.get_user_by_username(username):
            return "Username already taken."

        if self.user_service.get_user_by_email(email):
            return "Email already registered."

        return ""

    def login(self, email: str, password: str) -> str:
        user_dto = self.user_service.get_user_by_email(email)
        if user_dto and self.user_service.check_password(user_dto, password):
            if user_dto.is_verified:
                return True  # Indicate successful login
            return "Please verify your email before logging in."
        return "Invalid email or password."

    def verify_email(self, token: str) -> str:
        user_dto = self.user_service.verify_reset_token(token)
        if user_dto:
            user_dto.is_verified = True
            user_dto.verification_token = None
            self.user_service.update_user(user_dto)
            return "Email verification successful! You can now log in."
        return "Invalid or expired verification link."

    def resend_verification(self, email: str) -> str:
        user_dto = self.user_service.get_user_by_email(email)
        if not user_dto:
            return "No user found with this email address."

        if user_dto.is_verified:
            return "Your email is already verified."

        if (
            user_dto.last_verification_request
            and user_dto.last_verification_request
            > datetime.utcnow() - timedelta(minutes=5)
        ):
            return "Please wait before requesting another verification email."

        user_dto.verification_token = secrets.token_urlsafe(32)
        user_dto.last_verification_request = datetime.utcnow()
        self.user_service.update_user(user_dto)
        self._send_verification_email(user_dto)
        return "A new verification link has been sent to your email address."

    def _send_verification_email(self, user_dto: UserDTO):
        msg = Message(
            "Verify Your Email",
            sender="sereernest@gmail.com",
            recipients=[user_dto.email],
        )
        msg.body = f"""To verify your account, visit the following link:
{{url_for('verify', token=user_dto.verification_token, _external=True)}}
"""
        self.mail.send(msg)
