from flask_app import create_app
from flask_app.extensions import db
from instance.manager import (
    create_banners,
    create_categories,
    create_chats,
    create_default_currencies,
    create_topics,
)

app = create_app("instance.configs.development.DevelopmentConfig")


def initialize_database():
    with app.app_context():
        db.create_all()
        create_categories()
        create_topics()
        create_chats()
        create_default_currencies()
        create_banners()


if __name__ == "__main__":
    initialize_database()
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
