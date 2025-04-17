from datetime import datetime

from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from flask_app.extensions import db


class Currency(db.Model):
    __tablename__ = "currencies"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    coins = Column(Integer, default=0, nullable=False)  # Монеты
    stones = Column(Integer, default=0, nullable=False)  # Камни
    gems = Column(Integer, default=0, nullable=False)  # Гемы

    def __repr__(self) -> str:
        return f"<Currency user_id={self.user_id}, coins={self.coins}, stones={self.stones}, gems={self.gems}>"
