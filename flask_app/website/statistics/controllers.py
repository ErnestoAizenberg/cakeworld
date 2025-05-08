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
        result = (
            self.db_session.query(
                func.strftime("%Y-%m", User.created_at).label("month"),
                func.count(User.id).label("count"),
            )
            .group_by(func.strftime("%Y-%m", User.created_at))
            .order_by(func.strftime("%Y-%m", User.created_at))
            .all()
        )
        return [{"month": month, "count": count} for month, count in result]

    def fetch_message_sent_trends(self):
        result = (
            self.db_session.query(
                func.strftime("%Y-%m-%d", Message.created).label("day"),
                func.count(Message.id).label("count"),
            )
            .group_by(func.strftime("%Y-%m-%d", Message.created))
            .order_by(func.strftime("%Y-%m-%d", Message.created))
            .all()
        )
        return [{"day": day, "count": count} for day, count in result]

    def fetch_post_created_trends(self):
        result = (
            self.db_session.query(
                func.strftime("%Y-%m-%W", Post.created).label("week"),
                func.count(Post.id).label("count"),
            )
            .group_by(func.strftime("%Y-%m-%W", Post.created))
            .order_by(func.strftime("%Y-%m-%W", Post.created))
            .all()
        )
        return [{"week": week, "count": count} for week, count in result]

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
        result = (
            self.db_session.query(
                func.strftime("%Y-%m-%d", Message.created).label("day"),
                func.count(func.distinct(Message.user_id)).label("unique_users"),
            )
            .group_by(func.strftime("%Y-%m-%d", Message.created))
            .order_by(func.strftime("%Y-%m-%d", Message.created))
            .all()
        )
        return [
            {"day": day, "unique_users": unique_users} for day, unique_users in result
        ]

    def get_latest_data(self):
        latest_message_sent = self.get_latest_value(self.fetch_message_sent_trends())
        latest_post_created = self.get_latest_value(self.fetch_post_created_trends())
        latest_user_registration = self.get_latest_value(
            self.fetch_registration_trends()
        )

        return {
            "latest_message_sent": latest_message_sent,
            "latest_post_created": latest_post_created,
            "latest_user_registration": latest_user_registration,
        }

    def compile_statistics(self):
        return {
            "latest_data": self.get_latest_data(),
            "message_sent_trends": self.fetch_message_sent_trends(),
            "post_created_trends": self.fetch_post_created_trends(),
            "user_registration_trends": self.fetch_registration_trends(),
        }
