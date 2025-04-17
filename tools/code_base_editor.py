import os
import py_compile


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def log_history(action, history):
    history.append(action)


def replace_in_file(file_path, old_string, new_string):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content.replace(old_string, new_string)

    if content != new_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


def delete_from_file(file_path, string_to_delete):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content.replace(string_to_delete, "")

    if content != new_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


def replace_in_directory(directory, old_string, new_string, history):
    changes = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                if replace_in_file(file_path, old_string, new_string):
                    changes.append(file_path)
    return changes


def delete_from_directory(directory, string_to_delete, history):
    changes = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                if delete_from_file(file_path, string_to_delete):
                    changes.append(file_path)
    return changes


def check_syntax(directory):
    errors = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    py_compile.compile(filepath, doraise=True)
                except py_compile.PyCompileError as e:
                    errors.append(f"Ошибка в файле {filepath}: {e.msg}")
    return errors


def search_in_files(directory, search_string):
    results = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    if search_string in content:
                        results.append(filepath)
    return results


def show_help():
    help_message = (
        "Доступные команды:\n"
        "1. replace <old_string> <new_string> - Заменить строки в файлах .py.\n"
        "2. delete <string> - Удалить строки из файлов .py.\n"
        "3. check - Проверить синтаксис всех .py файлов.\n"
        "4. search <string> - Поиск строки в файлах .py.\n"
        "5. history - Показать историю изменений.\n"
        "6. help - Показать это сообщение.\n"
        "7. exit - Выход из редактора."
    )
    print(help_message)


def continue_prompt():
    input("\nНажмите Enter, чтобы продолжить...")


def main():
    history = []
    directory = input(
        "Введите путь к директории, где будут производиться операции: "
    ).strip()

    while True:
        clear_screen()
        print("Текущая директория:", directory)
        command = input("Введите команду (help для справки): ").strip().split()

        # Обработчик команд
        if command[0] == "replace":
            if len(command) < 3:
                print("Ошибка: не хватает аргументов для замены.")
                continue
            old_string = command[1]
            new_string = " ".join(command[2:])
            confirm = (
                input(
                    f"Вы действительно хотите заменить '{old_string}' на '{new_string}'? (y/n): "
                )
                .strip()
                .lower()
            )
            if confirm != "y":
                continue
            changes = replace_in_directory(directory, old_string, new_string, history)
            if changes:
                for file in changes:
                    print(f"Заменено в файле: {file}")
                log_history(
                    f"Заменено '{old_string}' на '{new_string}' в {len(changes)} файлах.",
                    history,
                )
            else:
                print("Не найдено строк для замены.")

        elif command[0] == "delete":
            if len(command) < 2:
                print("Ошибка: не указана строка для удаления.")
                continue
            string_to_delete = " ".join(command[1:])
            confirm = (
                input(
                    f"Вы действительно хотите удалить '{string_to_delete}' из файлов? (y/n): "
                )
                .strip()
                .lower()
            )
            if confirm != "y":
                continue
            changes = delete_from_directory(directory, string_to_delete, history)
            if changes:
                for file in changes:
                    print(f"Удалено из файла: {file}")
                log_history(
                    f"Удалено '{string_to_delete}' из {len(changes)} файлов.", history
                )
            else:
                print("Не найдено строк для удаления.")

        elif command[0] == "check":
            errors = check_syntax(directory)
            if errors:
                print("Ошибки синтаксиса обнаружены в следующих файлах:")
                print("\n".join(errors))
            else:
                print("Ошибок синтаксиса не найдено.")
            log_history("Проверка синтаксиса выполнена", history)

        elif command[0] == "search":
            if len(command) < 2:
                print("Ошибка: не указана строка для поиска.")
                continue
            search_string = " ".join(command[1:])
            results = search_in_files(directory, search_string)
            if results:
                print("Найдены файлы:")
                print("\n".join(results))
            else:
                print("Строка не найдена.")
            log_history(f"Поиск строки '{search_string}' завершен", history)

        elif command[0] == "history":
            if history:
                print("История изменений:")
                for record in history:
                    print(record)
            else:
                print("История изменений пуста.")

        elif command[0] == "help":
            show_help()

        elif command[0] == "exit":
            print("Выход из редактора.")
            break

        else:
            print("Неизвестная команда. Введите 'help' для справки.")

        # Запрос на продолжение после каждой команды
        continue_prompt()


if __name__ == "__main__":
    main()
