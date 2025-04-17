export class MessageLoader {
    constructor({ messagesContainer, chatId, userId, ownerId, limit }) {
        this.messagesContainer = messagesContainer;
        this.chatId = chatId;
        this.userId = userId;
        this.ownerId = ownerId;
        this.limit = limit;
        this.offsetTop = 0; // For older messages
        this.offsetBottom = 0; // For newer messages
        this.isLoading = false;
    }

    async loadInitialMessages() {
        try {
            const data = await this._fetchMessages(this.offsetBottom, this.limit);
            this._appendMessages(data.messages);
            this.offsetBottom += data.messages.length; // Update offset for newer messages
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }

    async loadOlderMessages() {
        if (this.isLoading) return;
        this.isLoading = true;

        try {
            const data = await this._fetchMessages(this.offsetTop, this.limit);
            this._prependMessages(data.messages);
            this.offsetTop += data.messages.length; // Update offset for older messages
        } catch (error) {
            console.error('Error loading older messages:', error);
        } finally {
            this.isLoading = false;
        }
    }

    async loadNewerMessages() {
        if (this.isLoading) return;
        this.isLoading = true;

        try {
            const data = await this._fetchMessages(this.offsetBottom, this.limit);
            this._appendMessages(data.messages);
            this.offsetBottom += data.messages.length; // Update offset for newer messages
        } catch (error) {
            console.error('Error loading newer messages:', error);
        } finally {
            this.isLoading = false;
        }
    }

    // offset parameter represents the current offset for loading messages
    async _fetchMessages(offset, limit) {
        const response = await fetch(`/load_direct_chat_messages?chat_id=${this.chatId}&owner_id=${this.ownerId}&offset=${offset}&limit=${limit}`);
        if (!response.ok) throw new Error('Network or server error');
        return response.json();
    }

    // Appending new messages to the container
    _appendMessages(messages) {
        const fragment = document.createDocumentFragment();
        messages.forEach(message => {
            const messageElement = this._createMessageElement(message);
            fragment.appendChild(messageElement);
        });
        this.messagesContainer.appendChild(fragment);
    }

    // Prepending older messages to the top of the container
    _prependMessages(messages) {
        const fragment = document.createDocumentFragment();
        messages.reverse().forEach(message => {
            const messageElement = this._createMessageElement(message);
            fragment.appendChild(messageElement);
        });
        this.messagesContainer.insertBefore(fragment, this.messagesContainer.firstChild);
    }

    // Creating HTML element for a message
    _createMessageElement(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', message.user_id === this.userId ? 'sent' : 'received');
        messageElement.setAttribute('data-id', message.id);

        const contentClass = message.user_id === this.userId ? 'user' : 'other'; 
        messageElement.innerHTML = `
        <!-- Message from user - "message-content user"
             Message from another user - "message-content other" -->
        <div class="message">
            <div class="message-content ${contentClass}">
                <p>${message.text}</p>
                <span class="timestamp">${message.created}</span>${message.is_read ? '<span>(Viewed)</span>' : ''}
            </div>    
        </div>`;

        return messageElement;
    }
  
}