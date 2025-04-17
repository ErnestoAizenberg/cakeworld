import os

def remove_comments_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    comment_count = 0
    
    for line in lines:
        original_line = line.strip()
        
        # Пропускаем строки, которые полностью являются комментариями
        if original_line.startswith('#'):
            comment_count += 1
            continue

        # Разделяем строку на код и комментарии
        comment_index = line.find('#')
        if comment_index != -1:
            # Если найден комментарий, добавляем только часть строки до комментария
            line_without_comment = line[:comment_index].rstrip() + '\n'
            new_lines.append(line_without_comment)
            comment_count += 1
        else:
            new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)  # Записываем измененные строки обратно в файл
    
    return comment_count

def remove_comments_from_directory(directory):
    total_comments_removed = 0
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            file_path = os.path.join(directory, filename)
            comments_removed = remove_comments_from_file(file_path)
            total_comments_removed += comments_removed
            print(f"Из файла '{filename}' удалено комментариев: {comments_removed}")
    
    print(f"\nОбщее количество удалённых комментариев: {total_comments_removed}")

if __name__ == "__main__":
    # Укажите директорию, в которой нужно удалить комментарии
    target_directory = '.'
    remove_comments_from_directory(target_directory)