# chat/message/models.py
from datetime import datetime

from flask_app.extensions import db


class Message(db.Model):
    """Database model for chat messages."""

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(800), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    images = db.Column(db.JSON, nullable=True, default=[])  # Stores image UUIDs as JSON
    views = db.Column(
        db.JSON, nullable=True, default=[]
    )  # Stores user_ids who viewed the message

    # Relationships
    user = db.relationship("User", backref="messages", lazy=True)
    reactions = db.relationship("Reaction", backref="message", lazy=True)

    def __repr__(self) -> str:
        return f"<Message id={self.id}, chat_id={self.chat_id}>"
