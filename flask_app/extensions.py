from flask_mail import Mail
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from flask_app.base.db.my_sqlalchemy import CustomSQLAlchemy

# Инициализация расширений без приложения
db = SQLAlchemy()
mail = Mail()
socketio = SocketIO()
csrf = CSRFProtect()


def init_extensions(app):
    """Ленивая инициализация расширений"""
    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    socketio.init_app(
        app, async_mode="eventlet", cors_allowed_origins="*", manage_session=False
    )
