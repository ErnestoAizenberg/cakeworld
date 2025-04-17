import os
import uuid
from io import BytesIO
from typing import Optional, Tuple

from flask import current_app
from PIL import Image

from flask_app.services import ImageService
from flask_app.utils import AvatarGenerator

font_path = "instance/DejaVuSans-Bold.ttf"
avatar_generator = AvatarGenerator(font_path=font_path)


class UserAvatarService:
    def __init__(self, image_service: ImageService, user_repo):
        self.image_service = image_service
        self.repo = user_repo

    def set_avatar(
        self,
        user: "User",
        img_data: Optional[BytesIO] = None,
        name: Optional[str] = None,
    ) -> None:
        previous_uuid = user.avatar_path
        new_uuid = str(uuid.uuid4())[:12]

        if img_data:
            full_image_path, _ = self.image_service.generate_path_by_uuid(new_uuid)
            self.image_service.process_image(img_data, full_image_path)
        else:
            full_image_path, _ = self.image_service.generate_path_by_uuid(new_uuid)
            if name:  # Проверка на наличие имени для генерации
                self.generate_avatar(name, full_image_path)

        user.avatar_path = new_uuid
        self.repo.save(user)

        if previous_uuid:
            self.remove_old_avatar(previous_uuid)

    def get_path_to_image(self, user: "User") -> str:
        if user.avatar_path:
            full_path, image_url = self.image_service.generate_path_by_uuid(
                user.avatar_path
            )
            if os.path.exists(full_path):
                return image_url
            else:
                current_app.logger.warning(
                    "Avatar file %s does not exist, generating a new one.", full_path
                )

        return self.generate_and_save_default_avatar(user)

    def remove_old_avatar(self, uuid: str):
        old_path, _ = self.image_service.generate_path_by_uuid(uuid)
        if os.path.exists(old_path):
            os.remove(old_path)

    def generate_and_save_default_avatar(self, user: "User") -> str:
        try:
            new_uuid = str(uuid.uuid4())[:12]
            full_image_path, url_path = self.image_service.generate_path_by_uuid(
                new_uuid
            )
            self.generate_avatar(name=None, save_path=full_image_path)
            user.avatar_path = new_uuid
            self.repo.save(user)
            return url_path
        except Exception as e:
            current_app.logger.error("Error generating default avatar: %s", e)
            return ""

    def generate_avatar(self, name: Optional[str], save_path: str):
        #
        avatar_generator.generate_avatar(name or "default_avatar", save_path)
