import os
import py_compile


def check_syntax_errors(directory):
    # Обходим все файлы и директории
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    # Пытаемся скомпилировать файл
                    py_compile.compile(filepath, doraise=True)
                except py_compile.PyCompileError as e:
                    print(f"Ошибка в файле {filepath}: {e.msg}")


if __name__ == "__main__":
    directory_to_check = "/storage/emulated/0/gitserver/cakeworld/clean/flask_app"
    check_syntax_errors(directory_to_check)
