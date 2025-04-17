document.addEventListener('DOMContentLoaded', function () {
    // Получаем данные из data-атрибутов
    const messagesContainer = document.getElementById('messages');
    if (!messagesContainer) {
        console.error('Элемент с id="messages" не найден');
        return;
    }

    const scrollToBottomButton = document.getElementById('scroll-to-bottom');
    if (!scrollToBottomButton) {
        console.error('Элемент с id="scroll-to-bottom" не найден');
        return;
    }

    const chatId = messagesContainer.dataset.chatId;
    const userId = messagesContainer.dataset.userId;
    const userUsername = messagesContainer.dataset.userUsername;
    const chatUrlName = messagesContainer.dataset.chatUrlName;
    const limit = isMobile() ? 20 : 50; // Разные лимиты для PC и мобильных устройств

    const messages = document.querySelectorAll('.message'); // Все сообщения
    const options = document.querySelector('.options'); // Меню опций
    const messageIdInput = options.querySelector('.message_id'); // Ввод для ID сообщения


    let isLoading = false; // Флаг для предотвращения множественных запросов
    let offsetTop = 0; // Смещение для подгрузки старых сообщений
    let offsetBottom = 0; // Смещение для подгрузки новых сообщений

    // Загружаем последние сообщения при загрузке страницы
    loadInitialMessages();

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

    // Функция для обновления счетчика непрочитанных сообщений
    function updateUnreadCounter() {
        const unreadMessages = document.querySelectorAll('.message:not([data-viewed="true"])');
        const unreadCount = unreadMessages.length;

        document.getElementById('unread-count').textContent = unreadCount;
    }

    // Функция для отслеживания просмотров сообщений
    function observeMessages() {
        const messages = document.querySelectorAll('.message');

        messages.forEach(message => {
            const observer = new IntersectionObserver(
                (entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const messageId = entry.target.dataset.id;
                            if (!entry.target.dataset.viewed) {
                                sendViewEvent(messageId); // Отправляем событие просмотра
                                entry.target.dataset.viewed = true; // Помечаем как просмотренное
                                updateUnreadCounter(); // Обновляем счетчик непрочитанных сообщений
                            }
                        }
                    });
                },
                { threshold: 0.5 } // Сообщение считается просмотренным, если видно 50%
            );

            observer.observe(message);
        });
    }

    // Функция для отправки события просмотра
    function sendViewEvent(messageId) {
        fetch(`/message/${messageId}/view`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: userId }),
        })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => {
                        throw new Error(`Ошибка сервера: ${text}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log('Просмотр сообщения зарегистрирован:', data);
            })
            .catch(error => {
                console.error('Ошибка при отправке события просмотра:', error);
            });
    }

    // Функция для загрузки начальных сообщений
    function loadInitialMessages() {
        fetch(`/load-chat-messages-feed?chat_id=${chatId}&offset=${offsetBottom}&limit=${limit}&user_id=${userId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка сети или сервера');
                }
                return response.json();
            })
            .then(data => {
                console.log('Загружены сообщения:', data.messages);

                if (data.messages.length > 0) {
                    const fragment = document.createDocumentFragment();
                    data.messages.forEach(message => {
                        const messageElement = createMessageElement(message);
                        fragment.appendChild(messageElement);
                    });

                    messagesContainer.appendChild(fragment);
                    offsetBottom += data.messages.length;

                    // Прокручиваем к последнему сообщению
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;

                    // Начинаем отслеживать просмотры
                    observeMessages();

                    // Обновляем счетчик непрочитанных сообщений
                    updateUnreadCounter();
                }
            })
            .catch(error => {
                console.error('Ошибка при загрузке сообщений:', error);
                showNotification('Ошибка при загрузке сообщений', 'error');
            });
    }

    // Функция для загрузки старых сообщений
    function loadOlderMessages() {
        if (isLoading) return; // Если уже загружаем, выходим
        isLoading = true;

        fetch(`/load-chat-messages-feed?chat_id=${chatId}&offset=${offsetTop}&limit=${limit}&user_id=${userId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка сети или сервера');
                }
                return response.json();
            })
            .then(data => {
                console.log('Загружены старые сообщения:', data.messages);

                if (data.messages.length > 0) {
                    const fragment = document.createDocumentFragment();
                    data.messages.reverse().forEach(message => {
                        const messageElement = createMessageElement(message);
                        fragment.insertBefore(messageElement, fragment.firstChild);
                    });

                    // Сохраняем текущую позицию скролла
                    const scrollTopBefore = messagesContainer.scrollTop;
                    const scrollHeightBefore = messagesContainer.scrollHeight;

                    messagesContainer.insertBefore(fragment, messagesContainer.firstChild);
                    offsetTop += data.messages.length;

                    // Восстанавливаем позицию скролла
                    messagesContainer.scrollTop = scrollTopBefore + (messagesContainer.scrollHeight - scrollHeightBefore);

                    // Начинаем отслеживать просмотры
                    observeMessages();

                    // Обновляем счетчик непрочитанных сообщений
                    updateUnreadCounter();
                }
            })
            .catch(error => {
                console.error('Ошибка при загрузке сообщений:', error);
                showNotification('Ошибка при загрузке сообщений', 'error');
            })
            .finally(() => {
                isLoading = false;
            });
    }

    // Функция для загрузки новых сообщений
    function loadNewerMessages() {
        if (isLoading) return; // Если уже загружаем, выходим
        isLoading = true;

        fetch(`/load-chat-messages-feed?chat_id=${chatId}&offset=${offsetBottom}&limit=${limit}&user_id=${userId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка сети или сервера');
                }
                return response.json();
            })
            .then(data => {
                console.log('Загружены новые сообщения:', data.messages);

                if (data.messages.length > 0) {
                    const fragment = document.createDocumentFragment();
                    data.messages.forEach(message => {
                        const messageElement = createMessageElement(message);
                        fragment.appendChild(messageElement);
                    });

                    messagesContainer.appendChild(fragment);
                    offsetBottom += data.messages.length;

                    // Начинаем отслеживать просмотры
                    observeMessages();

                    // Обновляем счетчик непрочитанных сообщений
                    updateUnreadCounter();
                }
            })
            .catch(error => {
                console.error('Ошибка при загрузке сообщений:', error);
                showNotification('Ошибка при загрузке сообщений', 'error');
            })
            .finally(() => {
                isLoading = false;
            });
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
                    <i class="fas fa-eye"></i> ${message.views.length}
                </div>
            </div>
        `;

        return messageElement;
    }

    // Обработчик прокрутки
    messagesContainer.addEventListener('scroll', () => {
        if (isLoading) return; // Если уже загружаем, выходим

        const { scrollTop, scrollHeight, clientHeight } = messagesContainer;

        // Загружаем старые сообщения при прокрутке вверх
        if (scrollTop === 0) {
            loadOlderMessages();
        }

        // Загружаем новые сообщения при прокрутке вниз
        if (scrollTop + clientHeight >= scrollHeight - 100) {
            loadNewerMessages();
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

        // Прокручиваем к новому сообщению, если пользователь уже внизу
        if (messagesContainer.scrollTop + messagesContainer.clientHeight >= messagesContainer.scrollHeight - 100) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        // Начинаем отслеживать просмотры
        observeMessages();

        // Обновляем счетчик непрочитанных сообщений
        updateUnreadCounter();
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

    // Обработчик кнопки "↓" для прокрутки вниз
    scrollToBottomButton.addEventListener('click', () => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });




let currentHighlightedMessage = null; // Для отслеживания выделенного сообщения

// Функция для очистки выделения
function clearHighlight() {
    if (currentHighlightedMessage) {
        currentHighlightedMessage.classList.remove('highlight'); // Убираем выделение
        currentHighlightedMessage = null; // Сбрасываем
    }
    options.style.display = 'none'; // Скрываем опции
}
function showOptions(message) {
    if (currentHighlightedMessage === message) {
        return; // Не делать ничего, если сообщение уже выделено
    }
    clearHighlight();
    message.classList.add('highlight');
    currentHighlightedMessage = message;
    messageIdInput.value = message.dataset.id;

    const rect = message.getBoundingClientRect();
    options.style.display = 'flex';
    options.style.top = `${rect.bottom + window.scrollY}px`;
    options.style.left = `${rect.left + window.scrollX}px`;
}


// Обработчик кликов по сообщениям
messages.forEach(message => {
    message.addEventListener('click', (event) => {
        event.stopPropagation(); // Предотвращаем всплытие события

        // Показываем меню опций для нажимаемого сообщения
        showOptions(message);
    });
});


document.addEventListener('click', (event) => {
    const message = event.target.closest('.message');
    if (message) {
        event.stopPropagation();
        showOptions(message);
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
            clearHighlight(); // Закрываем меню опций
        }).catch(err => {
            console.error('Ошибка копирования: ', err);
        });
    } else {
        console.error('Сообщение не найдено для ID:', messageId);
    }
}
// Функции для других опций (примеры)
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




});
