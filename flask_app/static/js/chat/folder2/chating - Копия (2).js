// Функция для отображения уведомления
function showNotification(message, status) {
    const notification = document.createElement('div');
    notification.className = `notification ${status}-notification`;
    notification.textContent = message;
    document.body.appendChild(notification);

    // Удаляем уведомление через 2 секунды
    setTimeout(() => {
        notification.remove();
    }, 2000);
}

// Получаем данные из data-атрибутов
const messagesContainer = document.getElementById('messages');
const chatId = messagesContainer.dataset.chatId;
const userId = messagesContainer.dataset.userId;
const userUsername = messagesContainer.dataset.userUsername;
const chatUrlName = messagesContainer.dataset.chatUrlName;
const limit = isMobile() ? 20 : 50; // Разные лимиты для PC и мобильных устройств

let isLoading = false; // Флаг для предотвращения множественных запросов
let offset = 0; // Смещение для подгрузки сообщений

// Загружаем последние сообщения при загрузке страницы
loadMessages();

// Функция для загрузки сообщений
function loadMessages() {
    if (isLoading) return; // Если уже загружаем, выходим
    isLoading = true;

    const loadingIndicator = document.getElementById('loadingIndicator');
    loadingIndicator.style.display = 'block';

    fetch(`/load-chat-messages-feed?chat_id=${chatId}&offset=${offset}&limit=${limit}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка сети или сервера');
            }
            return response.json();
        })
        .then(data => {
            console.log('Загружены сообщения:', data.messages); // Логируем загруженные сообщения

            if (data.messages.length > 0) {
                // Создаём DocumentFragment для улучшения производительности
                const fragment = document.createDocumentFragment();
                data.messages.reverse().forEach(message => {
                    const messageElement = createMessageElement(message);
                    fragment.insertBefore(messageElement, fragment.firstChild);
                });

                messagesContainer.insertBefore(fragment, messagesContainer.firstChild);
                offset += data.messages.length; // Увеличиваем смещение

                // Если сообщений больше, чем лимит, подгружаем следующую порцию заранее
                if (data.messages.length === limit) {
                    preloadMessages();
                }
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке сообщений:', error);
            showNotification('Ошибка при загрузке сообщений', 'error');
        })
        .finally(() => {
            isLoading = false;
            loadingIndicator.style.display = 'none';
        });
}

// Функция для предзагрузки сообщений
function preloadMessages() {
    const firstMessage = messagesContainer.firstElementChild;

    if (firstMessage) {
        const observer = new IntersectionObserver(
            (entries) => {
                if (entries[0].isIntersecting) {
                    loadMessages();
                    observer.disconnect();
                }
            },
            { threshold: 0.1 }
        );

        observer.observe(firstMessage);
    }
}

// Функция для проверки, является ли устройство мобильным
function isMobile() {
    return window.innerWidth <= 768; // Пример проверки для мобильных устройств
}

// Функция для создания элемента сообщения
function createMessageElement(message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', message.author === userUsername ? 'sent' : 'received');
    messageElement.setAttribute('data-id', message.id); // Добавим data-id для идентификации сообщения

    const imagesHTML = message.image_urls && message.image_urls.length > 0 
        ? `<div class="message-images">
             ${message.image_urls.map(url => `<img src="${url}" alt="Attached Image">`).join('')}
           </div>`
        : '';

    messageElement.innerHTML = `
        <div class="message-content">
            <span style="color:blue;">${message.author}:</span>
            ${message.text}
            ${imagesHTML}
            <div class="message-info">
                <span>${message.created}</span>
                <i class="fas fa-eye"></i> 0
            </div>
        </div>
    `;

    // Добавление обработчика события клика для отображения опций
    messageElement.addEventListener('click', () => {
        showOptions(messageElement);
    });

    return messageElement;
}

// Обработчик прокрутки
messagesContainer.addEventListener('scroll', () => {
    if (messagesContainer.scrollTop === 0) {
        loadMessages(); // Подгружаем сообщения при прокрутке вверх
    }
});

// Socket.IO
const socket = io();

// Присоединяемся к чату
socket.emit('join', { username: userUsername, room: chatUrlName });

// Обработка новых сообщений
socket.on('new_message', (data) => {
    const messageElement = createMessageElement(data);
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight; // Автоматическая прокрутка к новому сообщению
});

// Обработка отправки сообщения
document.getElementById('messageForm').addEventListener('submit', (e) => {
    e.preventDefault();

    const messageInput = document.getElementById('messageInput');
    const csrfToken = document.getElementById('csrfToken');
    const message = messageInput.value.trim();
    const imageInput = document.getElementById('imageInput');
    const formData = new FormData();

    if (!message && imageInput.files.length === 0) {
        showNotification('Пожалуйста, введите сообщение или выберите файл для отправки.', 'error');
        return;
    }

    // Добавляем данные сообщения
    formData.append('csrf_token', csrfToken.value);
    formData.append('user_id', userId);
    formData.append('chat_id', chatId);
    formData.append('message', message);

    // Добавляем изображения
    for (let i = 0; i < imageInput.files.length; i++) {
        formData.append('images[]', imageInput.files[i]);
    }

    // Отправляем данные на сервер
    fetch('/submit_message', {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    console.error('Server returned:', text);
                    throw new Error('Failed to send message');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                showNotification('Сообщение отправлено успешно!', 'success');
                messageInput.value = ''; // Очищаем текстовое поле
                imageInput.value = ''; // Очищаем поле выбора файла
            } else {
                throw new Error(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Не удалось отправить сообщение. Пожалуйста, попробуйте еще раз.', 'error');
        });
});

// Меню опций для сообщений
const options = document.querySelector('.options');
const messageIdInput = options.querySelector('.message_id');
let currentHighlightedMessage = null;

// Функция для очистки выделения
function clearHighlight() {
    if (currentHighlightedMessage) {
        currentHighlightedMessage.classList.remove('highlight');
        currentHighlightedMessage = null;
    }
    options.style.display = 'none';
}

// Функция для отображения меню опций
function showOptions(messageElement) {
    if (currentHighlightedMessage === messageElement) return;

    clearHighlight();
    messageElement.classList.add('highlight');
    currentHighlightedMessage = messageElement;
    messageIdInput.value = messageElement.dataset.id;

    const rect = messageElement.getBoundingClientRect();
    options.style.display = 'flex';
    options.style.top = `${rect.bottom + window.scrollY}px`;
    options.style.left = `${rect.left + window.scrollX}px`;
}

// Обработчик кликов по сообщениям
messagesContainer.addEventListener('click', (event) => {
    const messageElement = event.target.closest('.message');
    if (messageElement) {
        event.stopPropagation();
        showOptions(messageElement);
    } else if (!options.contains(event.target)) {
        clearHighlight();
    }
});

// Функция для копирования текста
function copyMessage() {
    const messageId = messageIdInput.value;
    const messageElement = document.querySelector(`.message[data-id="${messageId}"]`);

    if (messageElement) {
        const messageContent = messageElement.querySelector('.message-content').innerText;
        navigator.clipboard.writeText(messageContent).then(() => {
            showNotification('Сообщение скопировано!', 'success');
            clearHighlight();
        }).catch(err => {
            console.error('Ошибка копирования: ', err);
        });
    } else {
        console.error('Сообщение не найдено для ID:', messageId);
    }
}

// Функции для других опций
function replyToMessage() {
    const messageId = messageIdInput.value;
    console.log('Reply to message ID:', messageId);
    showNotification('Reply option clicked!', 'info');
}

function pinMessage() {
    const messageId = messageIdInput.value;
    console.log('Pin message ID:', messageId);
    showNotification('Pin option clicked!', 'info');
}

function deleteMessage() {
    const messageId = messageIdInput.value;
    console.log('Delete message ID:', messageId);
    showNotification('Delete option clicked!', 'info');
}

function reportMessage() {
    const messageId = messageIdInput.value;
    console.log('Report message ID:', messageId);
    showNotification('Report option clicked!', 'info');
}