from datetime import datetime

from flask_app.extensions import db


class BannedUser(db.Model):
    __tablename__ = "banned_users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    ban_until = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    ban_type = db.Column(
        db.String(50), nullable=False
    )  # Например, "post_publication", "reply_to_post"

    def is_banned(self) -> bool:
        """Проверяет, активен ли бан."""
        return self.ban_until > datetime.utcnow()
