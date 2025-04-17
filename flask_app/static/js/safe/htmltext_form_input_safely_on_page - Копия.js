document.addEventListener('DOMContentLoaded', function () {
    console.log('start');
    const inputField = document.getElementById('inputField');
    const outputDiv = document.getElementById('outputDiv');
    
    // Проверяем, что элементы правильно выбраны
    if (!inputField) {
        console.error('Не удалось найти элемент с id "inputField"');
        return; // Завершаем выполнение, если элемент не найден
    }
    if (!outputDiv) {
        console.error('Не удалось найти элемент с id "outputDiv"');
        return; // Завершаем выполнение, если элемент не найден
    }

    const allowedTags = [
        'b', 'i', 'u', 'strong', 'em', 'a', 'p', 'br', 'span', 'div', 'img', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'style'
    ];
    const allowedAttributes = {
        'a': ['href', 'title', 'target'],
        'img': ['src', 'alt', 'title'],
        '*': ['style', 'class']
    };

    inputField.addEventListener('input', function () {
        console.log('Содержимое ввода:', this.value); // Выводим текущее значение поля

        // Санитизируем введённый HTML
        const cleanHTML = DOMPurify.sanitize(this.value, {
            ALLOWED_TAGS: allowedTags,
            ALLOWED_ATTR: allowedAttributes
        });

        console.log('Санитизированное содержимое:', cleanHTML); // Выводим результат после санитации
        
        // Обновляем содержимое div
        outputDiv.innerHTML = cleanHTML;

        console.log('Обновлено содержимое outputDiv'); // Подтверждаем, что содержимое обновлено
    });
});