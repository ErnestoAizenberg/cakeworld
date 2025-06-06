import argparse
import os

from dotenv import load_dotenv

# Load environment variables from the specified .env file
load_dotenv("instance/env/.env")


def parse_arguments():
    """Parse command-line arguments for configuration overrides."""
    parser = argparse.ArgumentParser(description="Flask app with Redis support.")
    parser.add_argument("--server_address", type=str, help="URL of the server.")
    parser.add_argument("--secret_key", type=str, help="Secret key for Flask app.")
    parser.add_argument("--redis_host", type=str, help="Redis server host.")
    parser.add_argument("--redis_port", type=int, help="Redis server port.")
    parser.add_argument("--redis_db", type=int, help="Redis database number.")
    parser.add_argument("--host", type=str, help="Server host.")
    parser.add_argument("--port", type=int, help="Server port.")
    parser.add_argument(
        "--mail_username",
        type=str,
        help="Mail username, which will send emails to users (my_email@example.com).",
    )
    parser.add_argument(
        "--mail_password", type=str, help="Mail password or app-specific password."
    )

    return parser.parse_args()


# Parse command-line arguments
args = parse_arguments()


class Config:
    # Redis configuration
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_HOST = args.redis_host or os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = args.redis_port or int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = args.redis_db or int(os.getenv("REDIS_DB", 0))

    # Flask secret key
    SECRET_KEY = args.secret_key or os.getenv(
        "SECRET_KEY", "ktdkdgluurugifjGkmkyfvfhegegfbkegkenec"
    )

    # Upload folder
    UPLOAD_FOLDER = "static/uploads"

    # Database URI
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///forum.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email/SMS configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
    MAIL_USERNAME = args.mail_username or os.getenv(
        "MAIL_USERNAME", "sereernest@gmail.com"
    )
    MAIL_PASSWORD = args.mail_password or os.getenv("MAIL_PASSWORD")

    # OAuth2 providers
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
