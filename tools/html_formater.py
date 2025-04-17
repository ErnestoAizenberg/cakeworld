import re


class HtmlFormatter:
    def __init__(self, indentation="    "):
        self.indentation = indentation
        self.indent_level = 0

    def format_html(self, html):
        # Удаляем лишние пробелы и переносы строк вне тегов
        html = self.clean_whitespace(html)
        # Выравнивание HTML с учетом вложенности
        return self.indent_html(html)

    def clean_whitespace(self, html):
        # Убираем лишние пробелы и переносы строк
        html = re.sub(r"\s+", " ", html)  # Замена множества пробелов на один
        html = re.sub(r">\s+<", "><", html)  # Удаление пробелов между тегами
        return html.strip()

    def indent_html(self, html):
        formatted_html = ""
        tags = re.split(r"(<[^>]+>)", html)

        for tag in tags:
            if not tag.strip():
                continue
            if re.match(r"<\s*[^/][^>]*>", tag):  # Открывающий тег
                formatted_html += self.indent_level * self.indentation + tag + "\n"
                self.indent_level += 1
            elif re.match(r"<\s*/[^>]*>", tag):  # Закрывающий тег
                self.indent_level -= 1
                formatted_html += self.indent_level * self.indentation + tag + "\n"
            else:
                # Текстовое содержание
                formatted_html += (
                    self.indent_level * self.indentation + tag.strip() + "\n"
                )

        return formatted_html.strip()


def main():
    html_input = """
    <div>
        <p>{{ variable }}</p><span>{{ name }}</span>
        <div><h1>Title</h1>   <p>Text</p>  </div>
     <p> Another paragraph </p>
    </div>
    """

    formatter = HtmlFormatter()
    formatted_output = formatter.format_html(html_input)

    print("Formatted HTML:\n")
    print(formatted_output)


if __name__ == "__main__":
    main()
