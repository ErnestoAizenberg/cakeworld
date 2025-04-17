# run.py
import eventlet

from flask_app import create_app
from flask_app.extensions import db, socketio
from instance.manager import (create_banners, create_categories, create_chats,
                              create_default_currencies, create_topics)

app = create_app()


def initialize_database():
    with app.app_context():
        db.create_all()  # Создание всех таблиц
        create_categories()  # Создание категорий
        create_topics()  # Создание тем
        create_chats()  # Создание чатов
        create_default_currencies()
        create_banners()

        # Импортируем и активируем сигналы после создания всех необходимых таблиц
        from flask_app.models.signals import create_currency


if __name__ == "__main__":
    initialize_database()

    wrapped_socket = eventlet.wrap_ssl(
        eventlet.listen(("", 8443)),
        certfile="cert.pem",
        keyfile="key.pem",
        server_side=True,
    )
    eventlet.wsgi.server(wrapped_socket, app)
