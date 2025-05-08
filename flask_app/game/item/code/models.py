
from flask_app.extensions import db


class ItemCode(db.Model):
    __tablename__ = "item_codes"

    id = db.Column(db.Integer, primary_key=True)
    inventory_item_id = db.Column(
        db.Integer, db.ForeignKey("inventory_items.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_used = db.Column(db.Boolean, default=False)

    inventory_item = db.relationship("InventoryItem", backref="item_codes")
    user = db.relationship("User", backref="item_codes")

    def set_password(self, password: str) -> None:
        from flask_app.services import PasswordService

        self.password_hash = PasswordService.generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        from flask_app.services import PasswordService

        return PasswordService.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<ExchangeCode {self.password_hash}, used={self.is_used}, created={self.created_at}>"
