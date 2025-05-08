import logging
import os
import uuid
from functools import lru_cache
from io import BytesIO
from pathlib import Path
from typing import Any, Optional, Tuple

import redis
from flask import current_app


class AvatarService:
    def __init__(
        self,
        user_repo: Any,
        image_service: "ImageService",
        avatar_generator: "AvatarGenerator",
        redis_client: redis.Redis,
        files_location: str = "static/images/avatars",
        file_extension: str = ".png",
        path_division: int = 4,
    ):
        """
        Initialize the avatar service with dependencies and configuration.

        Args:
            user_repo: Repository for user data operations
            image_service: Service for image processing
            avatar_generator: Service for generating default avatars
            redis_client: Redis client for caching
            files_location: Base directory for avatar storage (relative to app root)
            file_extension: File extension for avatar images
            path_division: Number of characters to use for filename in UUID splitting
        """
        self.avatar_generator = avatar_generator
        self.image_service = image_service
        self.user_repo = user_repo
        self.redis_client = redis_client
        self.file_extension = (
            file_extension if file_extension.startswith(".") else f".{file_extension}"
        )
        self.path_division = path_division
        self.files_location = files_location

    @lru_cache(maxsize=512)
    def _generate_path_by_uuid(self, file_uuid: str) -> Tuple[str, str]:
        """
        Generate filesystem path and URL path for a given UUID with caching.

        Args:
            file_uuid: The UUID string to generate paths for

        Returns:
            Tuple of (absolute_filesystem_path, relative_url_path)

        Raises:
            ValueError: If the UUID is too short for the specified division
        """
        if len(file_uuid) < self.path_division * 2:
            raise ValueError(
                f"UUID must be at least {self.path_division * 2} characters long"
            )

        # Generate directory structure from UUID
        filename_part = file_uuid[-self.path_division :]
        dirname_part = file_uuid[: -self.path_division]
        dir_structure = os.path.sep.join(
            dirname_part[i : i + 2] for i in range(0, len(dirname_part), 2)
        )

        # Create paths
        relative_path = os.path.join(
            self.files_location, dir_structure, f"{filename_part}{self.file_extension}"
        )
        absolute_path = os.path.join(current_app.root_path, relative_path)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)

        return absolute_path, f"/{relative_path.replace(os.path.sep, '/')}"

    def get_user_avatar_or_generate(self, user_dto: "UserDTO") -> str:
        """
        Get existing user avatar or generate a default one if none exists.

        Args:
            user_dto: User data transfer object

        Returns:
            URL path to the avatar image
        """
        if user_dto.avatar_path:
            _, url_path = self._generate_path_by_uuid(user_dto.avatar_path)
            return url_path
        return self.generate_avatar(user_dto)

    def generate_avatar(self, user_dto: "UserDTO") -> str:
        """
        Generate and save a default avatar for the user.

        Args:
            user_dto: User data transfer object

        Returns:
            URL path to the generated avatar

        Raises:
            RuntimeError: If avatar generation fails
        """
        try:
            new_uuid = str(uuid.uuid4()).replace("-", "")[
                :16
            ]  # More collision-resistant
            full_path, url_path = self._generate_path_by_uuid(new_uuid)

            self.avatar_generator.generate_avatar(
                name=user_dto.username[:1].upper() if user_dto.username else "U",
                save_path=full_path,
            )

            user_dto.avatar_path = new_uuid
            self.user_repo.update(user_dto)

            return url_path

        except Exception as e:
            current_app.logger.error(
                "Error generating default avatar: %s", str(e), exc_info=True
            )
            raise RuntimeError("Failed to generate default avatar") from e

    def set_avatar(
        self,
        user_dto: "UserDTO",
        img_data: Optional[BytesIO] = None,
        name: Optional[str] = None,
        previous_uuid: Optional[str] = None,
    ) -> "UserDTO":
        """
        Set a new avatar for the user, either from image data or generated from name.

        Args:
            user_dto: User data transfer object
            img_data: Binary image data (optional)
            name: Name to use for generated avatar (optional)
            previous_uuid: Previous avatar UUID to clean up (optional)

        Returns:
            Updated user DTO

        Raises:
            ValueError: If neither img_data nor name is provided
        """
        if not img_data and not name:
            raise ValueError("Either img_data or name must be provided")

        new_uuid = str(uuid.uuid4()).replace("-", "")[:16]
        full_path, _ = self._generate_path_by_uuid(new_uuid)

        if img_data:
            self.image_service.process_image(img_data, full_path)
        else:
            self.avatar_generator.generate_avatar(
                name=name[:1].upper() if name else "U", save_path=full_path
            )

        user_dto.avatar_path = new_uuid
        updated_user = self.user_repo.update(user_dto)

        if previous_uuid:
            self._remove_old_avatar(previous_uuid)

        return updated_user

    def _remove_old_avatar(self, old_uuid: str) -> None:
        """
        Safely remove old avatar file if it exists.

        Args:
            old_uuid: UUID of the avatar to remove
        """
        try:
            old_path, _ = self._generate_path_by_uuid(old_uuid)
            if os.path.exists(old_path):
                os.remove(old_path)
            # Clear cache for this UUID
            self._generate_path_by_uuid.cache_clear()
        except Exception as e:
            current_app.logger.warning(
                "Failed to remove old avatar %s: %s", old_uuid, str(e)
            )

    def clear_cache(self) -> None:
        """Clear the path generation cache."""
        self._generate_path_by_uuid.cache_clear()
