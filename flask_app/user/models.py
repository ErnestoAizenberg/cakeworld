from datetime import datetime

from flask_app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(128), nullable=True)
    verification_token_expiry = db.Column(db.DateTime, nullable=True)
    last_verification_request = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    failed_login_attempts = db.Column(db.Integer, default=0)
    last_failed_login = db.Column(db.DateTime, nullable=True)
    avatar_path = db.Column(db.String(256), nullable=True)
    info = db.Column(db.Text, nullable=True)

    # Relationships
    topics = db.relationship("Topic", back_populates="author")
    posts = db.relationship("Post", back_populates="author")
