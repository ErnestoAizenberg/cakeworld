# flask_app/models/post.py
from datetime import datetime

from flask_app.extensions import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    images = db.Column(db.JSON, nullable=True)
    views = db.Column(
        db.JSON, nullable=True, default=lambda: []
    )  # user_id viewers list

    replies = db.relationship(
        "Post", backref=db.backref("parent_post", remote_side=[id]), lazy=True
    )

    def __repr__(self) -> str:
        return f"<Post id={self.id}, title={self.title}, user_id={self.user_id}>"
