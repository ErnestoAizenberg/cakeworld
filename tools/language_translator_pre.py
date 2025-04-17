import os


def search_flask_imports(base_directory):
    # Обходим все папки и файлы внутри указанной директории
    for root, dirs, files in os.walk(base_directory):
        for filename in files:
            # Проверяем, содержит ли имя файла "routes"
            if "routes" in filename:
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        # Читаем файл построчно
                        for line_number, line in enumerate(file, start=1):
                            if "from flask import" in line:
                                print(
                                    f"Found in {file_path} on line {line_number}: {line.strip()}"
                                )
                except (UnicodeDecodeError, FileNotFoundError) as e:
                    # Обработка ошибок при открытии файлов (например, бинарные файлы или отсутствующие)
                    print(f"Could not read file {file_path}. Error: {e}")


# Задаем базовую директорию для поиска
base_directory = "/storage/emulated/0/gitserver/cakeworld"
search_flask_imports(base_directory)
