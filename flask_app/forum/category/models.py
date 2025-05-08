
from flask_app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    color = db.Column(db.String(50))
    description = db.Column(db.Text)
    topics = db.relationship("Topic", backref="category_ref", lazy=True)

    def __repr__(self) -> str:
        return f"<Category id={self.id}, name={self.name}>"
