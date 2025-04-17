import logging
import os
import uuid
from io import BytesIO
from typing import Any, Optional

import redis
from flask import current_app


class AvatarService:
    def __init__(
        self,
        user_repo,
        image_service: "ImageService",
        avatar_generator: "AvatarGenerator",
        redis_client: redis.Redis,
    ):
        self.avatar_generator = avatar_generator
        self.image_service = image_service
        self.user_repo = user_repo
        self.redis_client = redis_client

    def get_user_avatar_or_generate(self, user_dto):
        if user_dto.avatar_path:
            avatar_path = self.image_service.generate_path_by_uuid(user_dto.avatar_path)
            return avatar_path
        else:
            return self.generate_avatar(user_dto)

    def generate_avatar(self, user_dto: "UserDTO") -> str:
        """Generate and save a default avatar for the user."""
        try:
            new_uuid = str(uuid.uuid4())[:12]
            full_image_path, url_path = self.image_service.generate_path_by_uuid(
                new_uuid
            )

            self.avatar_generator.generate_avatar(
                name="U",
                save_path=full_image_path,
            )
            user_dto.avatar_path = new_uuid
            self.user_repo.update(user_dto)

            return url_path

        except Exception as e:
            current_app.logger.error("Error generating default avatar: %s", e)
            return ""

    def set_avatar(
        self,
        user_dto: "UserDTO",
        img_data: Optional[BytesIO] = None,
        name: Optional[str] = None,
    ) -> "UserDTO":
        """Set the user's avatar either from provided image data or generate a new one."""
        previous_uuid = user_dto.avatar_path
        new_uuid = str(uuid.uuid4())[:12]
        full_image_path, _ = self.image_service.generate_path_by_uuid(new_uuid)

        if img_data:
            self.image_service.process_image(img_data, full_image_path)
        elif name:
            self.generate_avatar(name, full_image_path)
        else:
            raise ValueError("Invalid User Data")

        user_dto.avatar_path = new_uuid
        updated_user_dto = self.user_repo.update(user_dto)

        if previous_uuid:
            self.remove_old_avatar(previous_uuid)

        return updated_user_dto

    def remove_old_avatar(self, user_uuid: str) -> None:
        """Remove the old avatar from the filesystem if it exists."""
        old_path, _ = self.image_service.generate_path_by_uuid(user_uuid)
        if os.path.exists(old_path):
            os.remove(old_path)

    def generate_avatar(self, name: Optional[str], save_path: str) -> None:
        """Generate an avatar image and save it to the specified path."""
        self.avatar_generator.generate_avatar(name or "default_avatar", save_path)

    def get_cached_user_data(self, user_id: int) -> Optional[Any]:
        """Retrieve cached user data from Redis."""
        return self.redis_client.get(f"user:{user_id}")
