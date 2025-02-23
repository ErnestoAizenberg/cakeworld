from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

@app.route('/')
def index():
    # Mock data for the homepage
    latest_posts = [
        {"id": 1, "title": "New Update!", "summary": "Check out the latest features."},
        {"id": 2, "title": "Community Builds", "summary": "Explore amazing player creations."}
    ]
    return render_template('index.html', latest_posts=latest_posts)


@app.route('/create_thread')
def create_thread():
    return render_template('create_thread.html')

# technical_forum
@app.route('/technical_forums')
def technical_forums():
    return render_template('technical_forums.html')

# Mock данные для тем и постов
MOCK_TOPICS = {
    "bugs": {
        "title": "Баги",
        "posts": [
            {"id": 1, "title": "Ошибка при загрузке сервера", "author": "User1", "date": "2023-10-01", "views": 120},
            {"id": 2, "title": "Проблема с текстурами", "author": "User2", "date": "2023-10-02", "views": 95},
        ]
    },
    "youtube_cooperation": {
        "title": "Сотрудничество с YouTube",
        "posts": [
            {"id": 1, "title": "Как подать заявку на партнерство", "author": "Admin", "date": "2023-10-01", "views": 200}
        ]
    },
    "youtube_complaint": {
        "title": "Нарушение авторских прав",
        "posts": [
            {"id": 1, "title": "Нарушение Авторских прав с использованием моего контента 'https://youtube.com'", "author": "Userdzdox", "date": "2023-10-01", "views": 200}
        ]
    },
    "toimprove": {
        "title": "Поиск команды через билет",
        "posts": [
            {"id": 1, "title": "Предложение по добовлению функции...", "author": "Postman34", "date": "2023-10-01", "views": 200}
        ]
    },

    "notworking": {
        "title": "Не работает автоматическая перезагрузка",
        "posts": [
            {"id": 1, "title": "Сервер не перезагружается даже если он перезагружался вчера", "author": "Postman34", "date": "2023-10-01", "views": 200}
        ]
    },



@app.route('/thread/<int:thread_id>')
def thread(thread_id):
    # Mock данные для треда
    thread_data = {
        "title": "Ошибка при загрузке сервера",
        "author": "User1",
        "date": "2023-10-01",
        "views": 120,
        "content": "При загрузке сервера возникает ошибка 500. Кто-то сталкивался с этим?",
        "replies": [
            {
                "author": "User2",
                "author_avatar": "https://via.placeholder.com/50",
                "date": "2023-10-02",
                "content": "Попробуйте перезагрузить сервер."
            },
            {
                "author": "Admin",
                "author_avatar": "https://via.placeholder.com/50",
                "date": "2023-10-03",
                "content": "Мы уже работаем над исправлением этой ошибки."
            }
        ]
    }
    return render_template('thread.html', thread=thread_data)



# Categories Page
@app.route('/categories')
def categories():
    # Mock data for categories
    categories = [
        {"id": 1, "name": "Game Discussions", "icon": "message-circle"},
        {"id": 2, "name": "Mods & Plugins", "icon": "package"}
    ]
    return render_template('categories.html', categories=categories)

# Threads Page
@app.route('/threads')
def threads():
    # Mock data for threads
    discussion = {
        "id": 1,
        "title": "Best Minecraft Mods in 2023",
        "user": "Steve",
        "timestamp": "October 10, 2023",
        "content": "What are your favorite mods this year?",
        "replies": [
            {
                "id": 1,
                "user": "Alex",
                "avatar": "https://via.placeholder.com/40",
                "timestamp": "2 hours ago",
                "text": "I love OptiFine!"
            }
        ]
    }
    return render_template('threads.html', discussion=discussion)

# User Profile Page
@app.route('/profile')
def profile():
    # Mock data for user profile
    user = {
        "name": "Steve",
        "avatar": "https://via.placeholder.com/150",
        "joined": "October 2023",
        "activity": [
            "Posted in Best Minecraft Mods in 2023",
            "Commented on Community Builds"
        ]
    }
    return render_template('profile.html', user=user)

# Search Page
@app.route('/search')
def search():
    # Mock data for search results
    search_results = [
        {"id": 1, "title": "Search Result 1", "summary": "This is the first search result."},
        {"id": 2, "title": "Search Result 2", "summary": "This is the second search result."}
    ]
    return render_template('search.html', search_results=search_results)

# Admin Panel
@app.route('/admin')
def admin():
    # Mock data for admin panel
    admin_data = {
        "chart_data": {
            "width": 800,
            "height": 400,
            "color": "#8B4513"
        }
    }
    return render_template('admin.html', admin_data=admin_data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц в базе данных
    app.run(debug=True)