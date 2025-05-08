
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from flask_app.extensions import db


class InventoryItem(db.Model):
    __tablename__ = "inventory_items"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    store_item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, default=1)  # Количество экземпляров предмета

    user = relationship("User", backref="inventory_items", lazy=True)
    item = relationship("StoreItem", backref="inventory_items", lazy=True)

    def __repr__(self) -> str:
        return f"<InventoryItem user_id={self.user_id}, item_id={self.store_item_id}, quantity={self.quantity}>"
