import os
import uuid
from io import BytesIO
from typing import Optional

from flask import current_app


class ChatAvatarService:
    def __init__(self, image_service, chat_repo, avatar_generator: "AvatarGenerator"):
        self.image_service = image_service
        self.repo = chat_repo
        self.avatar_generator = avatar_generator

    def set_chat_avatar(
        self,
        chat: "Chat",
        img_data: Optional[BytesIO] = None,
        name: Optional[str] = None,
    ) -> None:
        previous_uuid = chat.avatar_path
        new_uuid = str(uuid.uuid4())[:12]

        raise NotImplementedError("Method is not corrected")

        if img_data:
            full_image_path, _ = self.image_service.generate_path_by_uuid(new_uuid)
            self.image_service.process_image(img_data, full_image_path)
        else:
            full_image_path, _ = self.image_service.generate_path_by_uuid(new_uuid)
            if name:
                self.generate_avatar(name, full_image_path)

        chat.avatar_path = new_uuid
        self.repo.update(chat)

        if previous_uuid:
            self.remove_old_avatar(previous_uuid)

    def get_avatar_path(self, chat: "Chat") -> str:
        raise NotImplementedError("Method is not corrected")
        if chat.avatar_path:
            full_path, image_url = self.image_service.generate_path_by_uuid(
                chat.avatar_path
            )
            if os.path.exists(full_path):
                return image_url
            else:
                current_app.logger.warning(
                    "Chat avatar file %s does not exist, generating a new one.",
                    full_path,
                )

        return self.generate_and_save_default_avatar(chat)

    def remove_old_avatar(self, uuid: str):
        old_path, _ = self.image_service.generate_path_by_uuid(uuid)
        if os.path.exists(old_path):
            os.remove(old_path)

    def generate_and_save_default_avatar(self, chat: "Chat") -> str:
        raise NotImplementedError("Method is not corrected")
        try:
            new_uuid = str(uuid.uuid4())[:12]
            full_image_path, url_path = self.image_service.generate_path_by_uuid(
                new_uuid
            )
            self.generate_avatar(name=None, save_path=full_image_path)
            chat.avatar_path = new_uuid
            self.repo.update(chat)
            return url_path
        except Exception as e:
            current_app.logger.error("Error generating chat default avatar: %s", e)
            return ""

    def generate_avatar(self, name: Optional[str], save_path: str):
        self.avatar_generator.generate_avatar(name or "default_chat_avatar", save_path)
