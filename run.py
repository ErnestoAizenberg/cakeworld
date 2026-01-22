from flask_app import Flask, create_app
from flask_app.extensions import db
from flask_sqlalchemy import SQLAlchemy

from instance.manager import (
    create_banners,
    create_categories,
    create_chats,
    create_default_currencies,
    create_topics,
)


def initialize_database(db: SQLAlchemy, app: Flask):
    with app.app_context():
        db.create_all()
        create_categories()
        create_topics()
        create_chats()
        create_default_currencies()
        create_banners()


if __name__ == "__main__":
    app: Flask = create_app("configs.development.DevelopmentConfig")
    initialize_database(db, app)
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
