import bleach
from bs4 import BeautifulSoup


def sanitize_html(html_content: str) -> str:
    """Очищает HTML от опасных тегов и атрибутов."""
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

    # Очистка HTML с использованием bleach
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

    return str(soup)
