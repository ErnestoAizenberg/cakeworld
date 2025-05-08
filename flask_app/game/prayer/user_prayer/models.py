from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from flask_app.extensions import db


class UserPray(db.Model):
    __tablename__ = "user_prays"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    banner_id = Column(
        Integer, ForeignKey("banners.id"), nullable=False
    )  # Внешний ключ на 'banners.id'
    created_at = Column(db.DateTime, default=datetime.utcnow)

    banner = relationship("Banner", backref="user_prays")
    user = relationship("User", backref="user_prays")

    def __repr__(self) -> str:
        return f"<UserPray id={self.id}, user_id={self.user_id}>"
