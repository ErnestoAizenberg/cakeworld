from flask_app.chat.public.models import Chat
from flask_app.extensions import db
from flask_app.forum.category.models import Category
from flask_app.forum.topic.models import Topic
from flask_app.game.banner.models import Banner
from flask_app.game.currency.models import Currency
from flask_app.user.models import User
from instance.data.initial_data import (BANNERS_DATA, CATEGORIES_DATA,
                                        CHATS_DATA, TOPICS_DATA)


def create_banners():
    for data in BANNERS_DATA:
        if not Banner.query.filter_by(title=data["title"]).first():
            banner = Banner(**data)
            db.session.add(banner)
            db.session.commit()
            print(f"Создан баннер: {banner.title}")


def create_categories():
    for name, description in CATEGORIES_DATA:
        if not Category.query.filter_by(name=name).first():
            category = Category(name=name, description=description)
            db.session.add(category)
            print(f"Создана категория: {name}")

    db.session.commit()
    print("Все категории успешно созданы!")


def create_topics():
    for data in TOPICS_DATA:
        category = db.session.query(Category).filter_by(id=data["category_id"]).first()

        if category:
            topic = Topic(**data)
            try:
                if not Topic.query.filter_by(url_name=topic.url_name).first():
                    db.session.add(topic)
                    db.session.commit()
                    print(f"Создана тема: {topic.title}")
                else:
                    print("Topic already exists, skip")
            except Exception as e:
                db.session.rollback()
                print(f"Ошибка при создании темы '{topic.title}': {str(e)}")
        else:
            print(f"Категория {data['category_id']} не найдена.")


def create_chats():
    for data in CHATS_DATA:
        if not Chat.query.filter_by(url_name=data["url_name"]).first():
            chat = Chat(**data)
            try:
                db.session.add(chat)
                db.session.commit()
                print(f"Создан чат: {chat.title}")
            except Exception as e:
                db.session.rollback()
                print(f"Ошибка при создании чата '{chat.title}': {str(e)}")


def create_default_currencies():
    users = User.query.all()
    for user in users:
        if not Currency.query.filter_by(user_id=user.id).first():
            currency = Currency(user_id=user.id)
            db.session.add(currency)
    db.session.commit()
