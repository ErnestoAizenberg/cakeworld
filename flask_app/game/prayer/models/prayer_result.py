from flask_app.extensions import db


class PrayerResult(db.Model):
    __tablename__ = "prayer_results"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    banner_id = db.Column(db.Integer, db.ForeignKey("prayers.id"), nullable=False)
    item_id = db.Column(
        db.Integer, db.ForeignKey("items.id"), nullable=True
    )  # id предмета, если выигрыш
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self) -> str:
        return f"<PrayerResult user_id={self.user_id}, banner_id={self.banner_id}, item_id={self.item_id}>"
