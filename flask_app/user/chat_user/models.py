
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from flask_app.extensions import db


class ChatUser(db.Model):
    __tablename__ = "chat_users"

    chat_id = db.Column(db.Integer, ForeignKey("chats.id"), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), primary_key=True)
    muted_until = db.Column(db.DateTime, nullable=True)

    user = relationship("User", backref="chat_users")

    def __repr__(self):
        return f"<ChatUser user_id={self.user_id}, chat_id={self.chat_id}, muted_until={self.muted_until}>"
