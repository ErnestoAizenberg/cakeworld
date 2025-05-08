from datetime import datetime

from sqlalchemy.orm import relationship

from flask_app.extensions import db


class Topic(db.Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url_name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    posts = relationship("Post", back_populates="topic", cascade="all, delete-orphan")
    category = relationship("Category", back_populates="topics")
    author = relationship("User", back_populates="topics")

    def get_post_count(self):
        return len(self.posts)

    def get_last_post(self):
        return max(self.posts, key=lambda post: post.created_at, default=None)
