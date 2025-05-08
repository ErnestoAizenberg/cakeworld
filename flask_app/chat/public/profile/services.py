import os
import uuid
from io import BytesIO
from typing import Optional

from flask import current_app


class ChatAvatarService:
    def __init__(
        self,
        user_repo,
        image_service: "ImageService",
        avatar_generator: "AvatarGenerator",
    ):
        self.avatar_generator = avatar_generator
        self.image_service = image_service
        self.repo = user_repo

    def get_path_to_image(self, user_dto: "UserDTO") -> str:
        """Get the path to the user's avatar image, generating a default if necessary."""
        if user_dto.avatar_path:
            full_path, image_url = self.image_service.generate_path_by_uuid(
                user_dto.avatar_path
            )
            if os.path.exists(full_path):
                return image_url
            else:
                current_app.logger.warning(
                    "Avatar file %s does not exist, generating a new one.", full_path
                )

        return self.generate_and_save_default_avatar(user_dto)

    def remove_old_avatar(self, uuid: str) -> None:
        """Remove the old avatar from the filesystem if it exists."""
        old_path, _ = self.image_service.generate_path_by_uuid(uuid)
        if os.path.exists(old_path):
            os.remove(old_path)

    def generate_and_save_default_avatar(self, user_dto: "UserDTO") -> str:
        """Generate and save a default avatar for the user."""
        try:
            new_uuid = str(uuid.uuid4())[:12]
            full_image_path, url_path = self.image_service.generate_path_by_uuid(
                new_uuid
            )
            self.generate_avatar(name=None, save_path=full_image_path)

            user_dto.avatar_path = new_uuid
            self.repo.update(user_dto)

            return url_path

        except Exception as e:
            current_app.logger.error("Error generating default avatar: %s", e)
            return ""

    def set_chat_avatar(
        self,
        user_dto: "UserDTO",
        img_data: Optional[BytesIO] = None,
        name: Optional[str] = None,
    ) -> "UserDTO":
        """Set the user's avatar either from provided image data or generate a new one."""
        previous_uuid = user_dto.avatar_path
        new_uuid = str(uuid.uuid4())[:12]

        if img_data:
            full_image_path, _ = self.image_service.generate_path_by_uuid(new_uuid)
            self.image_service.process_image(img_data, full_image_path)
        else:
            full_image_path, _ = self.image_service.generate_path_by_uuid(new_uuid)
            if name:
                self.generate_avatar(name, full_image_path)
            else:
                raise ValueError("Invalid User Data")

        user_dto.avatar_path = new_uuid
        updated_user_dto = self.repo.update(user_dto)

        if previous_uuid:
            self.remove_old_avatar(previous_uuid)

        return updated_user_dto

    def generate_avatar(self, name: Optional[str], save_path: str) -> None:
        """Generate an avatar image and save it to the specified path."""
        self.avatar_generator.generate_avatar(name or "default_avatar", save_path)
