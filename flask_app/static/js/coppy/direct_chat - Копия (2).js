import { MessageLoader } from './directMessageLoader.js';
import { MessageViewTracker } from './directMessageViewTracker.js';

export class Chat {
    constructor({ chatId, userId, ownerId, userUsername, chatUrlName, messagesContainer }) {
        this.chatId = chatId;
        this.userId = userId;
        this.userUsername = userUsername;
        this.chatUrlName = chatUrlName;
        this.ownerId = ownerId;
        this.messagesContainer = messagesContainer;

        console.log('Chat constructor called with:', { chatId, userId, userUsername, chatUrlName });

        this.unreadCountElement = document.getElementById('unread-count');
        this.scrollToBottomButton = document.getElementById('scroll-to-bottom');

        if (!this.messagesContainer || !this.unreadCountElement || !this.scrollToBottomButton) {
            console.error('One or more required elements are missing from the DOM.');
            return;
        }

        this.socket = io();
        console.log('Socket initialized:', this.socket);

        this.messageLoader = new MessageLoader({
            messagesContainer: this.messagesContainer,
            chatId: this.chatId,
            userId: this.userId,
            ownerId: this.ownerId,
            limit: 20
        });

        this.messageViewTracker = new MessageViewTracker(this.messagesContainer, this.userId);
        console.log('MessageLoader and MessageViewTracker instantiated.');

        this._initSocket();
        this._initEventListeners();
        this._initUnreadCounter();

        console.log('Loading initial messages');
        this.messageLoader.loadInitialMessages().then(() => {
            console.log('Initial messages loaded successfully.');
        }).catch(err => {
            console.error('Failed to load initial messages:', err);
        });
    }

    _initSocket() {
        this.socket.on('new_message', (data) => {
            console.log('Socket new_message received:', data);
            this._handleNewMessage(data);
        });
        console.log('Socket initialized for new messages');
    }

    _initUnreadCounter() {
        this.scrollToBottomButton.addEventListener('click', async () => {
            console.log('Scroll to bottom button clicked');
            this.scrollToBottomButton.disabled = true;
            this.scrollToBottomButton.innerHTML = '⌛ Loading...';

            try {
                const unreadMessages = await this._fetchUnreadMessages();
                console.log('Fetched unread messages:', unreadMessages);
                if (unreadMessages.length > 0) {
                    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
                    await this._markMessagesAsRead(unreadMessages);
                    this.unreadCountElement.textContent = 0;
                } else {
                    console.log('No unread messages to mark as read.');
                }
            } catch (error) {
                console.error('Error while handling unread messages:', error);
            } finally {
                this.scrollToBottomButton.disabled = false;
                this.scrollToBottomButton.innerHTML = '↓ Scroll to Bottom';
                console.log('Scroll to bottom button reset.');
            }
        });

        this.socket.on('update_unread_count', (data) => {
            console.log('Received unread count update:', data);
            if (data.user_id === this.userId) {
                this.unreadCountElement.textContent = data.unread_count;
                console.log('Updated unread count:', data.unread_count);
            }
        });
    }

    async _fetchUnreadMessages() {
        console.log(`Fetching unread messages for chat_id: ${this.chatId}, user_id: ${this.userId}`);
        const response = await fetch(`/get_unread_messages?chat_id=${this.chatId}&user_id=${this.userId}`);
        
        if (!response.ok) {
            console.error('Failed to fetch unread messages:', response.statusText);
            throw new Error('Failed to load unread messages');
        }

        const messages = await response.json();
        console.log('Unread messages successfully fetched:', messages);
        return messages;
    }

    async _markMessagesAsRead(messages) {
        console.log('Marking the following messages as read:', messages);
        for (const message of messages) {
            try {
                console.log(`Marking message ${message.id} as read.`);
                const response = await fetch(`/view_direct_message/${message.id}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: this.userId }),
                });
                
                if (!response.ok) {
                    console.error(`Failed to mark message ${message.id} as read:`, response.statusText);
                    throw new Error('Failed to mark message as read');
                }
            } catch (error) {
                console.error('Error marking the message as read:', error);
            }
        }
    }

    _initEventListeners() {
        console.log('Initializing event listeners');
        this.messagesContainer.addEventListener('scroll', () => this._handleScroll());
        console.log('Scroll event listener initialized for messages container');

        const messageForm = document.getElementById('messageForm');
        if (messageForm) {
            messageForm.addEventListener('submit', (e) => {
                console.log('Message form submitted');
                e.preventDefault();
                this._sendMessage();
            });
        } else {
            console.error('Message form not found in the DOM.');
        }

        this.messageViewTracker.init();
    }

    _sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const messageText = messageInput.value.trim();
        console.log('Attempting to send message:', messageText);

        if (!messageText) {
            console.warn('Message text is empty; not sending.');
            return;
        }

        console.log('Emitting send_message event:', { chat_id: this.chatId, user_id: this.userId, username: this.userUsername, text: messageText });
        this.socket.emit('send_message', {
            chat_id: this.chatId,
            user_id: this.userId,
            owner_id: this.ownerId,
            text: messageText,
       
        });

        messageInput.value = '';
        console.log('Message input cleared.');
    }

    _handleNewMessage(data) {
        console.log('Handling new received message:', data);
        const existingMessage = this.messagesContainer.querySelector(`[data-id="${data.id}"]`);

        if (existingMessage) {
            console.log('Message already exists in the container; ignoring:', data.id);
            return;
        }

        const messageElement = this.messageLoader._createMessageElement(data);
        this.messagesContainer.appendChild(messageElement);
        console.log('New message element created and appended.');

        const isNearBottom = this.messagesContainer.scrollTop + this.messagesContainer.clientHeight >= this.messagesContainer.scrollHeight - 100;
        console.log('Is near bottom of messages container:', isNearBottom);
        
        if (isNearBottom) {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
            console.log('Scrolled to the bottom of messages.');
        }

        if (data.user_id !== this.userId) {
            this.unreadCountElement.textContent = parseInt(this.unreadCountElement.textContent) + 1;
            console.log('Incremented unread count:', this.unreadCountElement.textContent);
        } else {
            console.log('Received own message, not incrementing unread count.');
        }
    }

    _handleScroll() {
        const { scrollTop, scrollHeight, clientHeight } = this.messagesContainer;
        console.log('Handling scroll event:', { scrollTop, scrollHeight, clientHeight });

        if (scrollTop === 0) {
            console.log('Scrolled to the top; loading older messages.');
            this.messageLoader.loadOlderMessages();
        }

        if (scrollTop + clientHeight >= scrollHeight - 100) {
            console.log('Near bottom; loading newer messages.');
            this.messageLoader.loadNewerMessages();
        }
    }
}