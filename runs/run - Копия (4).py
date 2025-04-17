import logging
import os
import signal
import time

import eventlet
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from flask_app import create_app
from flask_app.extensions import db, socketio
from instance.manager import (create_banners, create_categories, create_chats,
                              create_default_currencies, create_topics)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logging.getLogger("watchdog").setLevel(logging.WARNING)
logging.getLogger("eventlet").setLevel(logging.WARNING)

app = create_app()


def initialize_database():
    with app.app_context():
        db.create_all()
        create_categories()
        create_topics()
        create_chats()
        create_default_currencies()
        create_banners()


class ReloadHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_restart_time = 0
        self.restart_delay = 1  # Время задержки перезапуска

    def on_modified(self, event):
        # Игнорируем изменения в директории /.__gubrish__/
        if ".__gubrish__" in event.src_path:
            return

        # Проверяем, что это Python файл
        if not event.src_path.endswith(".py"):
            return

        # Проверим, прошло ли достаточно времени с последнего перезапуска
        current_time = time.time()
        if current_time - self.last_restart_time > self.restart_delay:
            logging.info("Изменения в файлах обнаружены. Перезапускаем сервер...")
            os.kill(os.getpid(), signal.SIGINT)  # Отправляем сигнал остановки
            self.last_restart_time = current_time


def start_server():
    wrapped_socket = eventlet.wrap_ssl(
        eventlet.listen(("", 8443)),
        certfile="instance/security/cert.pem",
        keyfile="instance/security/key.pem",
        server_side=True,
    )
    while True:
        eventlet.wsgi.server(wrapped_socket, app)  # Удалите блок try..except


if __name__ == "__main__":
    initialize_database()

    # Запускаем монитор файлов
    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    start_server()  # Без try..except, чтобы ошибки могли отображаться
    observer.stop()
    observer.join()
