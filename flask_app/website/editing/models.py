import bleach
from bs4 import BeautifulSoup

from flask_app.extensions import db


class Server(db.Model):
    __tablename__ = "servers"

    id = db.Column(db.Integer, primary_key=True)
    server_name = db.Column(db.String(120), nullable=True)
    server_description = db.Column(db.String(1000), nullable=True)
    server_background = db.Column(db.String(256), nullable=True)
    content_html = db.Column(db.Text, nullable=True)
    color_scheme = db.Column(db.String(7), nullable=True)  # HEX color code

    @classmethod
    def get_server(cls):
        """Получаем единственный экземпляр сервера."""
        server = cls.query.first()
        if server is None:
            server = cls()
            db.session.add(server)
            db.session.commit()
        return server

    def update_server(
        self,
        server_name=None,
        server_description=None,
        server_background=None,
        color_scheme=None,
    ):
        """Обновляем данные сервера."""
        if server_name is not None:
            self.server_name = server_name
        if server_description is not None:
            self.server_description = server_description
        if server_background is not None:
            self.server_background = server_background

        if color_scheme is not None:
            self.color_scheme = color_scheme

    def set_content_html(self, html_content):
        """Устанавливаем очищенное HTML-содержимое."""
        # Разрешенные теги и атрибуты
        ALLOWED_TAGS = [
            "a",
            "abbr",
            "acronym",
            "b",
            "blockquote",
            "code",
            "em",
            "i",
            "li",
            "ol",
            "strong",
            "ul",
            "p",
            "br",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
        ]
        ALLOWED_ATTRIBUTES = {
            "a": ["href", "title"],
            "abbr": ["title"],
            "acronym": ["title"],
        }

        # Очистка HTML от опасных тегов и атрибутов
        cleaned_html = bleach.clean(
            html_content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES
        )

        # Дополнительная проверка с помощью BeautifulSoup
        soup = BeautifulSoup(cleaned_html, "html.parser")
        for tag in soup.find_all():
            if tag.name not in ALLOWED_TAGS:
                tag.decompose()
            else:
                for attr in list(tag.attrs):
                    if attr not in ALLOWED_ATTRIBUTES.get(tag.name, []):
                        del tag[attr]

        final_html = str(soup)
        self.content_html = final_html  # Сохраняем очищенное содержимое

    def save(self):
        """Сохраняем изменения в базе данных."""
        db.session.commit()
