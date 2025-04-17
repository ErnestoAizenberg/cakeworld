from flask_app.extensions import db


class Prayer(db.Model):
    __tablename__ = "prayers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Integer, nullable=False)  # Стоимость молитвы в валюте
    description = db.Column(db.String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<Prayer id={self.id}, name={self.name}, cost={self.cost}>"
