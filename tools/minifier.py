import os

from htmlmin import minify as minify_html


def minify_html_file(input_file, output_file):
    """Минифицирует HTML файл."""
    with open(input_file, "r", encoding="utf-8") as f:
        minified = minify_html(f.read())
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(minified)


def process_directory(directory):
    """Рекурсивно обрабатывает директорию для минификации HTML файлов."""
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        if os.path.isdir(item_path):
            # Рекурсивный вызов для вложенных директорий
            process_directory(item_path)
        elif item.endswith(".html"):
            # Обработка HTML файла
            output_file = os.path.join(
                directory, "minified", item.replace(".html", ".min.html")
            )
            minify_html_file(item_path, output_file)
            print(f"Minified: {item_path} -> {output_file}")


def minify_all_html_files(base_template_dir):
    """Минифицирует все HTML файлы внутри заданного базового каталога."""
    process_directory(base_template_dir)


if __name__ == "__main__":
    paths = [
        "flask_app/user/templates",
        "forum/templates",
        "flask_app/game/templates",
        "flask_app/chat/templates",
        "flask_app/chat/public/templates",
        "flask_app/chat/direct/templates",
        "flask_app/chat/message/templates",
        "flask_app/forum/templates",
        "flask_app/forum/post/templates",
        "flask_app/forum/category/templates",
        "flask_app/game/templates",
        "flask_app/user/notification/templates",
        "flask_app/user/templates",
        "flask_app/chat/templates",
        "flask_app/website/templates",
        "flask_app/website/editing/templates",
        "flask_app/website/statistics/templates",
    ]

    for templates_directory in paths:
        minify_all_html_files(templates_directory)
