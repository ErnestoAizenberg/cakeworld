import { MessageLoader } from './messageLoader.js';
import { MessageViewTracker } from './messageViewTracker.js';

export class Chat {
    constructor(chatId, userId, userUsername, chatUrlName) {
        console.log('Chat constructor called with:', { chatId, userId, userUsername, chatUrlName });

        this.chatId = chatId;
        this.userId = userId;
        this.userUsername = userUsername;
        this.chatUrlName = chatUrlName;

        this.messagesContainer = document.getElementById('messages');
        console.log('Messages container:', this.messagesContainer);

        this.unreadCountElement = document.getElementById('unread-count');
        console.log('Unread count element:', this.unreadCountElement);

        this.socket = io();
        console.log('Socket initialized:', this.socket);

        this.messageLoader = new MessageLoader(this.messagesContainer, this.chatId, this.userId, 20);
        this.messageLoader.loadInitialMessages()
        console.log('MessageLoader initialized:', this.messageLoader);

        this.messageViewTracker = new MessageViewTracker(this.messagesContainer, this.userId);
        console.log('MessageViewTracker initialized:', this.messageViewTracker);

        this._initSocket();
        this._initEventListeners();
    }




    _initUnreadCounter() {
        // Обработчик клика по кнопке "Scroll to Bottom"
        this.scrollToBottomButton.addEventListener('click', () => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
            this.unreadCountElement.textContent = 0; // Сброс счетчика
        });
    }


_initUnreadCounter() {
    // Обработчик клика по кнопке "Scroll to Bottom"
    this.scrollToBottomButton.addEventListener('click', async () => {
        // Показываем анимацию загрузки
        this.scrollToBottomButton.disabled = true;
        this.scrollToBottomButton.innerHTML = '⌛ <span id="unread-count">0</span>';

        try {
            // Получаем все непрочитанные сообщения
            const unreadMessages = await this._fetchUnreadMessages();

            // Прокручиваем контейнер вниз
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;

            // Добавляем ID пользователя в просмотры для всех непрочитанных сообщений
            await this._markMessagesAsRead(unreadMessages);

            // Сбрасываем счетчик непрочитанных сообщений
            this.unreadCountElement.textContent = 0;
        } catch (error) {
            console.error('Ошибка при обработке непрочитанных сообщений:', error);
        } finally {
            // Восстанавливаем кнопку
            this.scrollToBottomButton.disabled = false;
            this.scrollToBottomButton.innerHTML = '↓ <span id="unread-count">0</span>';
        }
    });

    // Обновление счетчика при получении нового сообщения
    this.socket.on('update_unread_count', (data) => {
        console.log('Socket event "update_unread_count" received:', data);
        if (data.user_id == this.userId) {
            console.log('Updating unread count for current user:', data.unread_count);
            this.unreadCountElement.textContent = data.unread_count;
        } else {
            console.log('Unread count update is not for the current user.');
        }
    });
}

async _fetchUnreadMessages() {
    // Запрашиваем все непрочитанные сообщения с сервера
    const response = await fetch(`/get_unread_messages?chat_id=${this.chatId}&user_id=${this.userId}`);
    if (!response.ok) {
        throw new Error('Ошибка при загрузке непрочитанных сообщений');
    }
    return response.json();
}

async _markMessagesAsRead(messages) {
    // Отправляем запросы на сервер для отметки сообщений как прочитанных
    for (const message of messages) {
        try {
            const response = await fetch(`/message/${message.id}/view`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: this.userId }),
            });
            if (!response.ok) {
                throw new Error('Ошибка при отметке сообщения как прочитанного');
            }
        } catch (error) {
            console.error('Ошибка при обработке сообщения:', error);
        }
    }
}





    _initEventListeners() {
        console.log('Initializing event listeners...');

        // Обработчик прокрутки контейнера сообщений
        this.messagesContainer.addEventListener('scroll', () => {
            console.log('Scroll event detected on messages container.');
            this._handleScroll();
        });

        // Обработчик отправки формы сообщения
        const messageForm = document.getElementById('messageForm');
        if (messageForm) {
            messageForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this._sendMessage();
            });
        }

        // Инициализация отслеживания просмотра сообщений
        this.messageViewTracker.init();
        console.log('MessageViewTracker event listeners initialized.');
    }

    _sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const messageText = messageInput ? messageInput.value.trim() : '';

        if (!messageText) {
            console.log('Message is empty. Ignoring send request.');
            return;
        }

        console.log('Sending message:', messageText);

        // Отправка сообщения через Socket.IO
        this.socket.emit('send_message', {
            chat_id: this.chatId,
            user_id: this.userId,
            username: this.userUsername,
            text: messageText
        });

        // Очистка поля ввода
        if (messageInput) {
            messageInput.value = '';
        }
    }


_handleNewMessage(data) {
    console.log('Handling new message:', data);

    // Проверяем, есть ли сообщение с таким ID в контейнере
    const existingMessage = this.messagesContainer.querySelector(`[data-id="${data.id}"]`);
    if (existingMessage) {
        console.log('Message already exists. Skipping...');
        return;
    }

    const messageElement = this.messageLoader._createMessageElement(data);
    console.log('Message element created:', messageElement);

    this.messagesContainer.appendChild(messageElement);
    console.log('Message element appended to messages container.');

    const isNearBottom = this.messagesContainer.scrollTop + this.messagesContainer.clientHeight >= this.messagesContainer.scrollHeight - 100;
    console.log('Is near bottom:', isNearBottom);

    if (isNearBottom) {
        console.log('Scrolling to bottom...');
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    const isCurrentUserAuthor = data.user_id === this.userId;
    console.log('Is current user the author:', isCurrentUserAuthor, data.user_id, this.userId);

    if (!isCurrentUserAuthor) {
        const unreadCount = parseInt(this.unreadCountElement.textContent) + 1;
        console.log('Updating unread count:', unreadCount);
        this.unreadCountElement.textContent = unreadCount;
    } else {
        console.log('Message author is the current user. Unread count not updated.');
    }
}


_handleScroll() {
    // Получаем текущие значения прокрутки контейнера сообщений
    const { scrollTop, scrollHeight, clientHeight } = this.messagesContainer;

    // Выводим отладочную информацию о текущем состоянии прокрутки
    console.log('Scroll event handled. Scroll data:', {
        scrollTop,       // Текущее положение прокрутки (в пикселях от верха)
        scrollHeight,    // Общая высота содержимого контейнера (включая скрытую часть)
        clientHeight     // Видимая высота контейнера (высота области просмотра)
    });

    // Проверяем, достиг ли пользователь верха контейнера (прокрутка вверх)
    if (scrollTop === 0) {
        console.log('Scroll reached top. Loading older messages...');
        // Загружаем старые сообщения
        this.messageLoader.loadOlderMessages();
    }

    // Проверяем, находится ли пользователь вблизи низа контейнера (прокрутка вниз)
    if (scrollTop + clientHeight >= scrollHeight - 100) {
        console.log('Scroll near bottom. Loading newer messages...');
        // Загружаем новые сообщения
        this.messageLoader.loadNewerMessages();
    }
}
    
}