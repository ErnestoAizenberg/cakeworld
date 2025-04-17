from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, Secure World!"


if __name__ == "__main__":
    # Укажите путь к вашим сертификатам
    app.run(
        ssl_context=("~/mkcert/localhost.pem", "~/mkcert/localhost-key.pem"),
        host="0.0.0.0",
        port=5000,
    )
