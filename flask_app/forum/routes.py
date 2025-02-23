from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

from flask_app import app

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

# Mock data for usercontent
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

@app.route('/')
def index():
    latest_posts = [
        {"id": 1, "title": "New Update!", "summary": "Check out the latest features."},
        {"id": 2, "title": "Community Builds", "summary": "Explore amazing player creations."}
    ]
    return render_template('index.html', latest_posts=latest_posts)



# technical_forum
@app.route('/technical_forums')
def technical_forums():
    return render_template('technical_forums.html')


# inside a thread 
@app.route('/thread/<int:thread_id>')
def thread(thread_id):
    return render_template('thread.html', thread=thread_data)


# Threads Page
@app.route('/threads')
def threads():
    return render_template('threads.html', discussion=discussion)


# Categories Page
@app.route('/categories')
def categories():
    categories = [
        {"id": 1, "name": "Game Discussions", "icon": "message-circle"},
        {"id": 2, "name": "Mods & Plugins", "icon": "package"}
    ]
    return render_template('categories.html', categories=categories)




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