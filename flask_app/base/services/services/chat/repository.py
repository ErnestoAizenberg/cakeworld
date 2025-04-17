from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from sqlalchemy.exc import IntegrityError

from flask_app import db

from .models import (BannedUser, Chat, ChatUser, Currency, Message, Post,
                     Quest, QuestReward, StoreItem, User, UserQuest)

T = TypeVar("T", bound=db.Model)


# Определение обобщённого типа T
T = TypeVar("T")


class BaseRepository:
    def __init__(self, model: Type[T]):
        self.model = model

    def save(self, instance: T) -> Optional[T]:
        if not instance:
            return None

        try:
            db.session.add(instance)
            db.session.commit()
            return instance
        except IntegrityError:
            db.session.rollback()
            return None

    def get(self, id: int) -> Optional[T]:
        return self.model.query.get(id)

    def get_all(self, **filters: Dict[str, Any]) -> List[T]:
        query = self.model.query
        for key, value in filters.items():
            query = query.filter(getattr(self.model, key) == value)

        return query.all()  # Переместил return вне цикла

    def update(self, instance: T) -> Optional[T]:
        if not instance:
            return None

        try:
            db.session.commit()  # Предполагая, что изменения уже внесены в instance
            return instance
        except IntegrityError:
            db.session.rollback()
            return None

    def delete(self, instance: T) -> bool:
        if not instance:
            return False

        try:
            db.session.delete(instance)
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False


class BannedUserRepository(BaseRepository):
    def __init__(self):
        super().__init__(BannedUser)

    def get_active_bans_by_user_id(self, user_id: str) -> List[BannedUser]:
        return self.model.query.filter(
            self.model.user_id == user_id, self.model.ban_until > datetime.utcnow()
        ).all()


class ChatRepository(BaseRepository):
    def __init__(self):
        super().__init__(Chat)

    def get_chat_by_url(self, url_name: str) -> Chat:
        return db.session.query(Chat).filter(Chat.url_name == url_name).first()

    def create_chat(
        self, title: str, url_name: str, is_private: bool = False, description: str = ""
    ) -> Chat:
        chat = Chat(
            title=title,
            url_name=url_name,
            is_private=is_private,
            description=description,
        )
        return self.save(chat)

    def get_chat_by_id(self, chat_id: int) -> Chat:
        return self.get(chat_id)

    # Метод только для поиска, не создания
    def generate_url_name(self, user1_id: int, user2_id: int) -> str:
        """Генерирует уникальное имя URL для директ чата на основании ID пользователей."""
        return f"{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"


class ChatUserRepository(BaseRepository):
    def __init__(self):
        super().__init__(ChatUser)

    def get_user_chats(self, user_id: int) -> List[Chat]:
        return Chat.query.join(ChatUser).filter(ChatUser.user_id == user_id).all()

    def get_chat_users(self, chat_id: int) -> List[User]:
        chat = Chat.query.get(chat_id)
        if chat:
            return chat.users
        return []

    def get_chat_user(self, user_id: int, chat_id: int) -> Optional[ChatUser]:
        return self.model.query.filter_by(user_id=user_id, chat_id=chat_id).first()

    def approve_user(self, user_id: int, chat_id: int) -> Optional[ChatUser]:
        chat_user = self.get_chat_user(user_id, chat_id)
        if chat_user:
            chat_user.accepted = True
            db.session.commit()
        return chat_user

    def create_chat_user(
        self, user_id: int, chat_id: int, muted_until: Optional[datetime] = None
    ) -> ChatUser:
        return self.save(
            ChatUser(user_id=user_id, chat_id=chat_id, muted_until=muted_until)
        )


class CurrencyRepository(BaseRepository):
    def __init__(self):
        super().__init__(Currency)

    def get_currency_by_user_id(self, user_id: int) -> Optional[Currency]:
        return self.model.query.filter_by(user_id=user_id).first()


class MessageRepository(BaseRepository):
    def __init__(self):
        super().__init__(Message)

    def create_message(
        self, text: str, author: str, user_id: int, chat_id: int
    ) -> Message:
        """Создать новое сообщение."""
        return self.save(
            Message(text=text, author=author, user_id=user_id, chat_id=chat_id)
        )

    def get_chat_messages(
        self, chat_id: int, offset: int, limit: int, user_id: int
    ) -> List[Message]:
        """Получить сообщения чата."""
        return self.query.filter_by(chat_id=chat_id).offset(offset).limit(limit).all()

    def view_message(self, message_id: int, user_id: int) -> Optional[Message]:
        """Отметить сообщение как просмотренное."""
        message = self.get(message_id)  # Метод из BaseRepository
        if message:
            message.views.append(
                user_id
            )  # Добавление пользователя в список просмотревших
            self.save(message)  # Сохраняем изменения
            return message
        return None

    def get_unread_count(self, chat_id: int, user_id: int) -> int:
        """Получить количество непрочитанных сообщений."""
        unread_msg_count = (
            db.session.query(Message)
            .filter(
                Message.chat_id == chat_id,
                Message.user_id != user_id,
                ~Message.views.contains(user_id),
            )
            .count()
        )
        return unread_msg_count


class PostRepository(BaseRepository):
    def __init__(self):
        super().__init__(Post)

    def create_post(
        self,
        title: str,
        content: str,
        user_id: int,
        topic_id: int,
        post_id: Optional[int] = None,
    ) -> Post:
        return self.save(
            Post(
                title=title,
                content=content,
                user_id=user_id,
                topic_id=topic_id,
                post_id=post_id,
            )
        )


class PrayerRepository(BaseRepository):
    def __init__(self):
        super().__init__(Prayer)

    def get_user_prayer_count(self, user_id: int) -> int:
        """Возвращает количество молитв пользователя за последние 24 часа."""
        from datetime import datetime, timedelta

        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        return PrayerResult.query.filter(
            PrayerResult.user_id == user_id,
            PrayerResult.created_at >= twenty_four_hours_ago,
        ).count()


class QuestRepository(BaseRepository):
    def __init__(self):
        super().__init__(Quest)

    def get_active_quests(self) -> List[Quest]:
        return self.model.query.filter_by(is_active=True).all()


class QuestRewardRepository(BaseRepository):
    def __init__(self):
        super().__init__(QuestReward)

    def get_rewards_by_quest_id(self, quest_id: int) -> List[QuestReward]:
        return self.model.query.filter_by(quest_id=quest_id).all()


class UserQuestRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserQuest)

    def get_user_quests(self, user_id: int) -> List[UserQuest]:
        return self.model.query.filter_by(user_id=user_id).all()


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.model.query.filter_by(username=username).first()


class StoreItemRepository(BaseRepository):
    def __init__(self):
        super().__init__(StoreItem)
        # provided methods: save, get, get_all, update, delete
