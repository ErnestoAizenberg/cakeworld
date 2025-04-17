import { MessageLoader } from './messageLoader.js';
import { MessageViewTracker } from './messageViewTracker.js'; 

export class Chat {
    constructor(chatId, userId, userUsername, chatUrlName, csrfToken ) {
        console.log('Chat constructor called with:', { chatId, userId, userUsername, chatUrlName });

        this.chatId = chatId;
        this.userId = userId;
        this.userUsername = userUsername;
        this.chatUrlName = chatUrlName;
        this.csrfToken = csrfToken;

        // Инициализация элементов DOM
        this.messagesContainer = document.getElementById('messages');
        console.log('Messages container:', this.messagesContainer);
        if (!this.messagesContainer) {
            console.error('Messages container not found!');
        }

        this.unreadCountElement = document.getElementById('unread-count');
        console.log('Unread count element:', this.unreadCountElement);
        if (!this.unreadCountElement) {
            console.error('Unread count element not found!');
        }

        this.scrollToBottomButton = document.getElementById('scroll-to-bottom');
        console.log('Scroll to bottom button:', this.scrollToBottomButton);
        if (!this.scrollToBottomButton) {
            console.error('Scroll to bottom button not found!');
        }

        // Инициализация сокета
        this.socket = io();
        console.log('Socket initialized:', this.socket);
        if (!this.socket) {
            console.error('Socket initialization failed!');
        }

        // Инициализация MessageLoader
        this.messageLoader = new MessageLoader({
            messagesContainer: this.messagesContainer,
            chatId: this.chatId,
            userId: this.userId,
            limit: 20
        });
        console.log('MessageLoader initialized:', this.messageLoader);

        // Загрузка начальных сообщений
        this.messageLoader.loadInitialMessages();
        console.log('Initial messages loaded.');

        // Инициализация MessageViewTracker
        this.messageViewTracker = new MessageViewTracker(this.messagesContainer, this.userId);
        console.log('MessageViewTracker initialized:', this.messageViewTracker);

        // Инициализация сокета и обработчиков событий
        this._initSocket();
        this._initEventListeners();
        this._initUnreadCounter();
    }

    _initSocket() {
        console.log('Initializing socket...');

        // Подключение к комнате чата
        this.socket.emit('join', { username: this.userUsername, room: this.chatUrlName });
        console.log('Socket emit "join" with:', { username: this.userUsername, room: this.chatUrlName });

        // Обработчик нового сообщения
        this.socket.on('new_message', (data) => {
            console.log('Socket event "new_message" received:', data);
            this._handleNewMessage(data);
        });

        // Обработчик обновления счетчика непрочитанных сообщений
        this.socket.on('update_unread_count', (data) => {
            console.log('Socket event "update_unread_count" received:', data);
            if (data.user_id === this.userId) {
                console.log('Updating unread count for current user:', data.unread_count);
                this.unreadCountElement.textContent = data.unread_count;
            } else {
                console.log('Unread count update is not for the current user.');
            }
        });
    }

    _initUnreadCounter() {
        console.log('Initializing unread counter...');

        if (!this.scrollToBottomButton) {
            console.error('Scroll to bottom button not found.');
            return;
        }

        // Обработчик клика по кнопке "Scroll to Bottom"
        this.scrollToBottomButton.addEventListener('click', () => {
            console.log('Scroll to bottom button clicked.');
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
            console.log('Scrolled to bottom.');

            // Сбрасываем счетчик непрочитанных сообщений
            this.unreadCountElement.textContent = 0;
            console.log('Unread count reset to 0.');
        });
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
                console.log('Message form submitted.');
                this._sendMessage();
            });
        } else {
            console.error('Message form not found!');
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

        console.log('[DEBUG] Sending message:', messageText);

        // Отправка сообщения через Socket.IO
        this.socket.emit('send_message_in_chat', {
            chat_id: this.chatId,
            user_id: this.userId,
            username: this.userUsername,
            text: messageText
        });


        // Очистка поля ввода
        if (messageInput) {
            console.log('[DEBUG] cleaning input content:', messageInput);
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

        // Создаем элемент сообщения и добавляем его в контейнер
        const messageElement = this.messageLoader._createMessageElement(data);
        this.messagesContainer.appendChild(messageElement);
        console.log('Message element appended to messages container.');

        // Прокрутка вниз, если пользователь находится вблизи низа
        const isNearBottom = this.messagesContainer.scrollTop + this.messagesContainer.clientHeight >= this.messagesContainer.scrollHeight - 100;
        if (isNearBottom) {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
            console.log('Scrolled to bottom after new message.');
        }

        // Обновление счетчика непрочитанных сообщений
        if (data.user_id !== this.userId) {
            const unreadCount = parseInt(this.unreadCountElement.textContent) + 1;
            this.unreadCountElement.textContent = unreadCount;
            console.log('Unread count updated:', unreadCount);
        }
    }

    _handleScroll() {
        const { scrollTop, scrollHeight, clientHeight } = this.messagesContainer;
        console.log('Scroll event handled. Scroll data:', { scrollTop, scrollHeight, clientHeight });

        // Загрузка старых сообщений при прокрутке вверх
        if (scrollTop === 0) {
            console.log('Scroll reached top. Loading older messages...');
            this.messageLoader.loadOlderMessages();
        }

        // Загрузка новых сообщений при прокрутке вниз
        if (scrollTop + clientHeight >= scrollHeight - 100) {
            console.log('Scroll near bottom. Loading newer messages...');
            this.messageLoader.loadNewerMessages();
        }
    }
}