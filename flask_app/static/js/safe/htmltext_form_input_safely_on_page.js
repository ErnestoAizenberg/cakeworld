// Конфигурация для DOMPurify
const config = {
  ALLOWED_TAGS: [
    // Список разрешенных тегов
    'a', 'b', 'blockquote', 'br', 'caption', 'code', 'div', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'hr', 'i', 'img', 'li', 'ol', 'p', 'pre', 'small', 'span', 'strike', 'strong', 'sub', 'sup',
    'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr', 'u', 'ul'
  ],
  ALLOWED_ATTR: ['style', 'class'], // Разрешаем атрибуты style и class
  ALLOW_DATA_ATTR: false, // Запрещаем data-атрибуты
  FORBID_TAGS: ['script', 'iframe', 'frame', 'object', 'embed'] // Запрещаем опасные теги
};

// Функция для очистки HTML
function sanitizeHTML(html) {
  return DOMPurify.sanitize(html, config);
}

// Обработчик события DOMContentLoaded
document.addEventListener('DOMContentLoaded', function () {
  console.log('start');

  const inputField = document.getElementById('inputField');
  const outputDiv = document.getElementById('outputDiv');

  // Обработчик события input для inputField
  inputField.addEventListener('input', function () {
    console.log('Содержимое ввода:', this.value);

    const cleanHTML = sanitizeHTML(this.value);
    console.log('Санитизированное содержимое:', cleanHTML);

    outputDiv.innerHTML = cleanHTML; // Обновляем содержимое outputDiv
    console.log('Обновлено содержимое outputDiv');
  });
});