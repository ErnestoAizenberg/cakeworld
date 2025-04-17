from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository

from .dtos import UserDTO
from .models import User


class UserRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(User, UserDTO, db_session)

    def _to_dto(self, user: User) -> UserDTO:
        """Convert User model to UserDTO with proper null checks"""
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            is_verified=user.is_verified,
            verification_token=user.verification_token,
            verification_token_expiry=user.verification_token_expiry,
            last_verification_request=user.last_verification_request,
            created_at=user.created_at,
            last_login=user.last_login,
            failed_login_attempts=user.failed_login_attempts,
            last_failed_login=user.last_failed_login,
            avatar_path=user.avatar_path,
            info=user.info,
        )

    def _from_dto(self, dto: UserDTO) -> User:
        """Convert UserDTO to User model, handling partial updates"""
        user = User(
            username=dto.username,
            email=dto.email,
            password_hash=dto.password_hash,
            is_verified=dto.is_verified,
            verification_token=dto.verification_token,
            verification_token_expiry=dto.verification_token_expiry,
            avatar_path=dto.avatar_path,
            info=dto.info,
        )

        # Only set these if explicitly provided
        if dto.id is not None:
            user.id = dto.id
        if dto.last_verification_request is not None:
            user.last_verification_request = dto.last_verification_request
        if dto.last_login is not None:
            user.last_login = dto.last_login
        if dto.failed_login_attempts is not None:
            user.failed_login_attempts = dto.failed_login_attempts
        if dto.last_failed_login is not None:
            user.last_failed_login = dto.last_failed_login

        return user

    def get_user_by_username(self, username: str) -> Optional[UserDTO]:
        """Gets user by username."""
        instance = (
            self.db_session.query(self.model).filter_by(username=username).first()
        )
        return self._to_dto(instance) if instance else None

    def get_user_by_email(self, email: str) -> Optional[UserDTO]:
        """Gets user by email."""
        instance = self.db_session.query(self.model).filter_by(email=email).first()
        return self._to_dto(instance) if instance else None

    def get_user_by_verification_token(self, token: str) -> Optional[UserDTO]:
        """Gets user by verification token."""
        instance = (
            self.db_session.query(self.model)
            .filter_by(verification_token=token)
            .first()
        )
        return self._to_dto(instance) if instance else None

    def get_user_by_password_reset_token(self, token: str) -> Optional[UserDTO]:
        """Gets user by password reset token."""
        instance = (
            self.db_session.query(self.model)
            .filter_by(password_reset_token=token)
            .first()
        )
        return self._to_dto(instance) if instance else None

    def increment_failed_login_attempts(self, user_dto: UserDTO) -> None:
        """Increments failed login attempts counter."""
        user = self.db_session.query(self.model).get(user_dto.id)
        if user:
            user.failed_login_attempts += 1
            user.last_failed_login = datetime.utcnow()
            self.db_session.commit()

    def reset_failed_login_attempts(self, user_dto: UserDTO) -> None:
        """Resets failed login attempts counter."""
        user = self.db_session.query(self.model).get(user_dto.id)
        if user:
            user.failed_login_attempts = 0
            user.last_failed_login = None
            self.db_session.commit()

    def update_last_login(self, user_dto: UserDTO) -> None:
        """Updates last login time."""
        user = self.db_session.query(self.model).get(user_dto.id)
        if user:
            user.last_login = datetime.utcnow()
            self.db_session.commit()

    def count_user_posts(self, user_id):
        this_user = self.db_session.query(self.model).get(user_id)
        # but not self.get as it will return dto
        return len(this_user.posts)
