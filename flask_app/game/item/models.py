
from sqlalchemy import Column, Integer, String, Text

from flask_app.extensions import db


class StoreItem(db.Model):
    __tablename__ = "items"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price_coins = Column(Integer, nullable=True)  # Стоимость в монетах
    price_gems = Column(Integer, nullable=True)  # Стоимость в гемах
    image_path = Column(String(256), nullable=False)
    rarity = Column(Integer, nullable=False)  # Редкость (3, 4, 5)

    def __repr__(self) -> str:
        return f"<StoreItem id={self.id}, name={self.name}{self.description}-{self.price_coins}-{self.price_gems}-{self.image_path}-{self.rarity}>"
