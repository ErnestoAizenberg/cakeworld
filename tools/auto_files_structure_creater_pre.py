import os

# Определяем базовую директорию для проекта
base_dir = "flask_app"

# Определяем необходимые директории и файлы
directories_and_files = {
    "config": "",
    "run.py": "",
    os.path.join(base_dir, "fabric.py"): "",
    os.path.join(
        base_dir, "forum", "templates", "some_template.html"
    ): "<html>\n<head>\n    <title>Forum Template</title>\n</head>\n<body>\n    <h1>This is a forum template</h1>\n</body>\n</html>",
    os.path.join(
        base_dir, "game", "templates", "other_template.html"
    ): "<html>\n<head>\n    <title>Game Template</title>\n</head>\n<body>\n    <h1>This is a game template</h1>\n</body>\n</html>",
    os.path.join(
        base_dir, "user", "templates", "user_template.html"
    ): "<html>\n<head>\n    <title>User Template</title>\n</head>\n<body>\n    <h1>This is a user template</h1>\n</body>\n</html>",
    os.path.join(
        base_dir, "chat", "templates", "chat_template.html"
    ): "<html>\n<head>\n    <title>Chat Template</title>\n</head>\n<body>\n    <h1>This is a chat template</h1>\n</body>\n</html>",
    os.path.join(
        base_dir, "website", "templates", "server_page.html"
    ): "<html>\n<head>\n    <title>Server Page</title>\n</head>\n<body>\n    <h1>This is the server page template</h1>\n</body>\n</html>",
}


# Функция для создания структуры директорий и файлов
def create_structure():
    for path, content in directories_and_files.items():
        # Получаем директорию по пути файла
        directory = os.path.dirname(path)

        # Создаем директорию, если она не существует
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Создаем файл и записываем в него содержимое
        with open(path, "w") as f:
            f.write(content)

    print("Файловая структура создана успешно!")


# Запуск функции создания структуры
if __name__ == "__main__":
    create_structure()
