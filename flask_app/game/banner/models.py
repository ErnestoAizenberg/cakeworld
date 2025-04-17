from datetime import datetime

from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from flask_app.extensions import db


class Banner(db.Model):
    __tablename__ = "banners"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(256), nullable=False)
    created_at = Column(db.DateTime, default=datetime.utcnow)

    logic = Column(
        JSON, nullable=True
    )  # JSON для хранения сложной логики (шансы, гарантии и т.д.)

    def __repr__(self) -> str:
        return f"<Banner id={self.id}, title={self.title}>"
