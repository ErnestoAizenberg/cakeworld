document.addEventListener('DOMContentLoaded', function () { console.log('start'); const inputField = document.getElementById('inputField'); const outputDiv = document.getElementById('outputDiv');

const allowedAttributes = { 'a': ['href', 'title', 'target'], 'img': ['src', 'alt', 'title'], 'span': ['style', 'class'], // Убедитесь, что указаны атрибуты для конкретных тегов 'div': ['style', 'class'], // и здесь '*': [] // Отключите '*' или укажите только те атрибуты, которые действительно нужны };



 inputField.addEventListener('input', function () { console.log('Содержимое ввода:', this.value); const cleanHTML = DOMPurify.sanitize(this.value, { ALLOWED_TAGS: allowedTags, ALLOWED_ATTR: allowedAttributes }); console.log('Санитизированное содержимое:', cleanHTML); outputDiv.innerHTML = cleanHTML; console.log('Обновлено содержимое outputDiv'); }); });