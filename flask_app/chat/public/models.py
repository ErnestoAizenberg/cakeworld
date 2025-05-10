from sqlalchemy.orm import relationship

from flask_app.extensions import db


class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    url_name = db.Column(
        db.String(120),
        # unique=True,
        nullable=False,
    )
    is_private = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(1000))
    avatar_path = db.Column(db.String(256), nullable=True)

    messages = relationship("Message", backref="chat", lazy=True)
    # users = relationship('ChatUser', backref='chat', lazy=True)
    users = relationship("User", secondary="chat_users", backref="chats")

    def __repr__(self) -> str:
        return f"<Chat id={self.id}, title={self.title}, is_private={self.is_private}>"
