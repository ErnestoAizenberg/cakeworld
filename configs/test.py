from dotenv import load_dotenv
from .config import Config

load_dotenv("instance/env/.env")


class TestConfig(Config):
    PORT = 5000
    HOST = "127.0.0.1"
