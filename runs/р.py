import os
import subprocess
import sys

from flask import Flask

# Создание Flask приложения
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, Secure World!"


# Функция для установки mkcert
def install_mkcert():
    print("Установка mkcert...")
    if sys.platform == "linux":
        subprocess.run(["apt", "install", "libnss3-tools"], check=True)
    elif sys.platform == "darwin":
        subprocess.run(["brew", "install", "mkcert"], check=True)

    # Установка mkcert
    subprocess.run(["mkcert", "-install"], check=True)


# Функция для создания сертификатов
def create_certificates():
    print("Создание сертификатов...")
    subprocess.run(["mkcert", "localhost"], check=True)


def main():
    # Убедитесь, что у нас установлен mkcert
    try:
        subprocess.run(["mkcert", "-version"], check=True)
    except subprocess.CalledProcessError:
        install_mkcert()

    # Создание сертификатов
    create_certificates()

    # Запуск Flask приложения с SSL
    context = (
        "localhost.pem",
        "localhost-key.pem",
    )  # Используем сгенерированные сертификаты
    app.run(host="0.0.0.0", port=443, ssl_context=context)


if __name__ == "__main__":
    main()
