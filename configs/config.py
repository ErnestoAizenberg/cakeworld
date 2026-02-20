import os
from typing import Final, Dict

from dotenv import load_dotenv

# Load environment variables from the specified .env file
load_dotenv(".env")


class Config:
    # Redis configuration
    REDIS_URL: Final[str] = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_HOST: Final[str] = os.getenv("REDIS_HOST", "localhost")
    REDIS_POR: Final[int] = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: Final[int] = int(os.getenv("REDIS_DB", 0))

    # Flask secret key
    SECRET_KEY: Final[str] = os.getenv(
        "SECRET_KEY", "ktdkdgluurugifjGkmkyfvfhegegfbkegkenec"
    )

    # Upload folder
    UPLOAD_FOLDER: Final[str] = "static/uploads"

    # Database URI
    SQLALCHEMY_DATABASE_URI: Final[str] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///forum.db")
    SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False

    # Email/SMS configuration
    MAIL_SERVER: Final[str] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT: Final[int] = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS: Final[bool] = os.getenv("MAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
    MAIL_USERNAME: Final[str] = os.getenv(
        "MAIL_USERNAME", "sereernest@gmail.com"
    )
    MAIL_PASSWORD: Final[str] = os.getenv("MAIL_PASSWORD", "")

    # OAuth2 providers
    OAUTH2_PROVIDERS: Final[Dict[str, dict]] = {
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
