import os

from dotenv import load_dotenv

load_dotenv("instance/env/.env")


class Config:
    REDIS_URL = "redis://localhost:6379/0"
    SECRET_KEY = "ktdkdgluurugifjGkmkyfvfhegegfbkegkenec"
    UPLOAD_FOLDER = "static/uploads"
    SQLALCHEMY_DATABASE_URI = "sqlite:///forum.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ENGINE_OPTIONS = {'autoflush': False}
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    OAUTH2_PROVIDERS = {
        "google": {
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET"),
            "authorize_url": "https://accounts.google.com/o/oauth2/auth",
            "token_url": "https://accounts.google.com/o/oauth2/token",
            "userinfo": {
                "url": "https://www.googleapis.com/oauth2/v3/userinfo",
                "email": lambda json: json["email"],
            },
            "scopes": ["https://www.googleapis.com/auth/userinfo.email"],
        },
    }
