import os

from dotenv import load_dotenv

load_dotenv("instance/env/.env")


class TestConfig:
    # Используйте SQLite в памяти для тестирования
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Выставим секретный ключ для тестов
    SECRET_KEY = "test_secret_key"

    # Отключим Redis для тестирования
    REDIS_URL = None

    # Настройте e-mail сервер для тестирования
    MAIL_SERVER = "smtp.test.com"  # Используйте заглушку вместо настоящего сервиса
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("TEST_MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("TEST_MAIL_PASSWORD", "")

    OAUTH2_PROVIDERS = {}


def load_test_config(app):
    app.config.from_object(TestConfig)
