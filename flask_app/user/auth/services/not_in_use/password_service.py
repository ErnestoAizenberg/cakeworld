from typing import Optional

from flask import current_app
from itsdangerous import URLSafeSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash


class PasswordService:
    @staticmethod
    def generate_password_hash(password: str) -> str:
        return generate_password_hash(password)

    @staticmethod
    def check_password_hash(password_hash: str, password: str) -> bool:
        return check_password_hash(password_hash, password)


class TokenService:
    @staticmethod
    def generate_reset_token(user_id: int, expires_sec=1800) -> str:
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": user_id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token) -> Optional[int]:
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
            return user_id
        except Exception as e:
            raise ValueError(str(e))
