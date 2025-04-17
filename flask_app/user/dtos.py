from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserDTO:
    """Data Transfer Object for User operations"""

    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    verification_token: Optional[str] = None
    verification_token_expiry: Optional[datetime] = None
    last_verification_request: Optional[datetime] = None
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    failed_login_attempts: int = 0
    last_failed_login: Optional[datetime] = None
    avatar_path: Optional[str] = None
    info: Optional[str] = None
    last_password_reset_request: Optional[datetime] = None

    # Exclude sensitive data from serialization
    def to_dict(self, include_sensitive=False):
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "avatar_path": self.avatar_path,
            "info": self.info,
        }
        if include_sensitive:
            data.update(
                {
                    "last_login": (
                        self.last_login.isoformat() if self.last_login else None
                    ),
                    "failed_login_attempts": self.failed_login_attempts,
                    "last_failed_login": (
                        self.last_failed_login.isoformat()
                        if self.last_failed_login
                        else None
                    ),
                }
            )
        return data
