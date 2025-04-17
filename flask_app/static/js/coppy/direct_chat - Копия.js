import { MessageLoader } from './directMessageLoader.js';
import { MessageViewTracker } from './directMessageViewTracker.js';

export class Chat {
    constructor(chatId, userId, userUsername, chatUrlName) {
        this.chatId = chatId;
        this.userId = userId;
        this.userUsername = userUsername;
        this.chatUrlName = chatUrlName;

        this.messagesContainer = document.getElementById('messages');
        this.unreadCountElement = document.getElementById('unread-count');
        this.scrollToBottomButton = document.getElementById('scroll-to-bottom');

        this.socket = io();
        this.messageLoader = new MessageLoader(this.messagesContainer, this.chatId, this.userId, 20);
        this.messageViewTracker = new MessageViewTracker(this.messagesContainer, this.userId);

        this._initSocket();
        this._initEventListeners();
        this._initUnreadCounter();

        // Load initial messages
        this.messageLoader.loadInitialMessages();
    }

    _initSocket() {
        this.socket.on('new_message', (data) => this._handleNewMessage(data));
    }

    _initUnreadCounter() {
        this.scrollToBottomButton.addEventListener('click', async () => {
            this.scrollToBottomButton.disabled = true;
            this.scrollToBottomButton.innerHTML = '⌛ Loading...';

            try {
                const unreadMessages = await this._fetchUnreadMessages();
                this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
                await this._markMessagesAsRead(unreadMessages);
                this.unreadCountElement.textContent = 0;
            } catch (error) {
                console.error('Error handling unread messages:', error);
            } finally {
                this.scrollToBottomButton.disabled = false;
                this.scrollToBottomButton.innerHTML = '↓ Scroll to Bottom';
            }
        });

        this.socket.on('update_unread_count', (data) => {
            if (data.user_id === this.userId) {
                this.unreadCountElement.textContent = data.unread_count;
            }
        });
    }

    async _fetchUnreadMessages() {
        const response = await fetch(`/get_unread_messages?chat_id=${this.chatId}&user_id=${this.userId}`);
        if (!response.ok) throw new Error('Failed to load unread messages');
        return response.json();
    }

    async _markMessagesAsRead(messages) {
        for (const message of messages) {
            try {
                const response = await fetch(`/view_direct_message/${message.id}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ user_id: this.userId }),
                });
                if (!response.ok) throw new Error('Failed to mark message as read');
            } catch (error) {
                console.error('Error marking message as read:', error);
            }
        }
    }

    _initEventListeners() {
        this.messagesContainer.addEventListener('scroll', () => this._handleScroll());
        
        const messageForm = document.getElementById('messageForm');
        if (messageForm) {
            messageForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this._sendMessage();
            });
        }

        this.messageViewTracker.init();
    }

    _sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const messageText = messageInput.value.trim();

        if (!messageText) return;

        this.socket.emit('send_message', {
            chat_id: this.chatId,
            user_id: this.userId,
            username: this.userUsername,
            text: messageText,
        });

        messageInput.value = '';
    }

    _handleNewMessage(data) {
        const existingMessage = this.messagesContainer.querySelector(`[data-id="${data.id}"]`);
        if (existingMessage) return;

        const messageElement = this.messageLoader._createMessageElement(data);
        this.messagesContainer.appendChild(messageElement);
        
        const isNearBottom = this.messagesContainer.scrollTop + this.messagesContainer.clientHeight >= this.messagesContainer.scrollHeight - 100;
        if (isNearBottom) this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;

        if (data.user_id !== this.userId) {
            this.unreadCountElement.textContent = parseInt(this.unreadCountElement.textContent) + 1;
        }
    }

    _handleScroll() {
        const { scrollTop, scrollHeight, clientHeight } = this.messagesContainer;

        if (scrollTop === 0) {
            this.messageLoader.loadOlderMessages();
        }

        if (scrollTop + clientHeight >= scrollHeight - 100) {
            this.messageLoader.loadNewerMessages();
        }
    }
}