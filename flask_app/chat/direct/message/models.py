from datetime import datetime
from typing import List, Optional

from flask_app.extensions import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(800), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    images = db.Column(
        db.JSON, nullable=True, default=[]
    )  # Хранение UUID изображений в формате JSON
    reactions = db.relationship("Reaction", backref="message", lazy=True)
    views = db.Column(
        db.JSON, nullable=True, default=[]
    )  # Список user_id, которые просмотрели сообщение
    user = db.relationship(
        "User", foreign_keys=[user_id], backref="messages", lazy=True
    )

    user = db.relationship("User", backref="messages", lazy=True)

    def __repr__(self) -> str:
        return f"<Message id={self.id}, chat_id={self.chat_id}>"

    def add_view(self, user_id: int) -> None:
        """Добавляет user_id к списку просмотров, если он еще не добавлен."""
        if user_id not in self.views:
            self.views.append(user_id)
            db.session.commit()

    def get_views(self) -> List[int]:
        """Возвращает список user_id, которые просмотрели сообщение."""
        return self.views or []

    def get_views_amount(self) -> int:
        """Возвращает количество уникальных пользователей, просмотревших сообщение."""
        return len(self.get_views())

    def set_text(self, text: str) -> None:
        """Устанавливает текст сообщения."""
        self.text = text
        db.session.commit()

    def add_image(self, image_file) -> Optional[str]:
        """Добавляет изображение и возвращает его UUID."""
        from ..services.image_service import \
            ImageService  # Логика работы с изображениями вынесена в сервис

        image_uuid = ImageService.save_image(image_file)
        if image_uuid:
            self.images.append(image_uuid)
            db.session.commit()
        return image_uuid

    def get_image_url(self, image_uuid: str) -> Optional[str]:
        """Возвращает URL изображения по его UUID."""
        from ..services.image_service import ImageService

        return ImageService.get_image_url(image_uuid)

    def get_all_image_urls(self) -> List[str]:
        """Возвращает список URL всех изображений."""
        return [self.get_image_url(uuid) for uuid in self.images] if self.images else []

    def delete_image(self, image_uuid: str) -> None:
        """Удаляет изображение по его UUID."""
        from flask_app.services.image_service import ImageService

        if image_uuid in self.images:
            ImageService.delete_image(image_uuid)
            self.images.remove(image_uuid)
            db.session.commit()
