import logging
import os
import uuid
from io import BytesIO
from typing import Any, Optional

import redis
from flask import current_app

from flask_app.user.exceptions import UsernameAlreadyExistsError, UserNotFoundError


class ProfileService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def update_info(self, user_dto: "UserDTO"):
        raise NotImplementedError("The method is not implemented yet")

    def update_username(self, user_dto: int, new_username: str) -> Optional["UserDTO"]:
        user = self.user_repo.get(user_dto.id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")

        existing_user = self.user_repo.get_user_by_username(new_username)
        if existing_user and existing_user.id != user.id:
            raise UsernameAlreadyExistsError(
                f"Username '{new_username}' already exists"
            )

        user.username = new_username
        self.user_repo.save(user)
        return user
