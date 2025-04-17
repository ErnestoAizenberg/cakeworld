from sqlalchemy import func
from sqlalchemy.orm import Session

from flask_app.chat.message.models import Message
from flask_app.chat.public.models import Chat
from flask_app.forum.post.models import Post
from flask_app.user.models import User


class SiteStatsController:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_latest_value(self, trends):
        return trends[-1] if trends else None

    def fetch_registration_trends(self):
        return (
            self.db_session.query(
                func.strftime("%Y-%m", User.created_at).label("month"),
                func.count(User.id).label("count"),
            )
            .group_by("month")
            .order_by("month")
            .all()
        )

    def fetch_message_sent_trends(self):
        return (
            self.db_session.query(
                func.strftime("%Y-%m-%d", Message.created).label("day"),
                func.count(Message.id).label("count"),
            )
            .group_by("day")
            .order_by("day")
            .all()
        )

    def fetch_post_created_trends(self):
        return (
            self.db_session.query(
                func.strftime("%Y-%m-%W", Post.created).label("week"),
                func.count(Post.id).label("count"),
            )
            .group_by("week")
            .order_by("week")
            .all()
        )

    def fetch_chat_user_counts(self):
        chats = self.db_session.query(Chat).all()
        return [
            {
                "chat_id": chat.id,
                "chat_title": chat.title,
                "user_count": chat.users.count(),
            }
            for chat in chats
        ]

    def fetch_unique_user_trends(self):
        return (
            self.db_session.query(
                func.strftime("%Y-%m-%d", Message.created).label("day"),
                func.count(func.distinct(Message.user_id)).label("unique_users"),
            )
            .group_by("day")
            .order_by("day")
            .all()
        )
