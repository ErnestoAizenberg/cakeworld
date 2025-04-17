export class MessageLoader {
    constructor(messagesContainer, chatId, userId, limit) {
        this.messagesContainer = messagesContainer;
        this.chatId = chatId;
        this.userId = userId;
        this.limit = limit;
        this.offsetTop = 0;
        this.offsetBottom = 0;
        this.isLoading = false;
    }

    async loadInitialMessages() {
        try {
            const data = await this._fetchMessages(this.offsetBottom);
            this._appendMessages(data.messages);
            this.offsetBottom += data.messages.length;
        } catch (error) {
            console.error('Ошибка при загрузке сообщений:', error);
        }
    }

    async loadOlderMessages() {
        if (this.isLoading) return;
        this.isLoading = true;

        try {
            const data = await this._fetchMessages(this.offsetTop);
            this._prependMessages(data.messages);
            this.offsetTop += data.messages.length;
        } catch (error) {
            console.error('Ошибка при загрузке старых сообщений:', error);
        } finally {
            this.isLoading = false;
        }
    }

    async loadNewerMessages() {
        if (this.isLoading) return;
        this.isLoading = true;

        try {
            const data = await this._fetchMessages(this.offsetBottom);
            this._appendMessages(data.messages);
            this.offsetBottom += data.messages.length;
        } catch (error) {
            console.error('Ошибка при загрузке новых сообщений:', error);
        } finally {
            this.isLoading = false;
        }
    }

    async _fetchMessages(offset) {
        const response = await fetch(`/load-chat-messages-feed?chat_id=${this.chatId}&offset=${offset}&limit=${this.limit}&user_id=${this.userId}`);
        if (!response.ok) throw new Error('Ошибка сети или сервера');
        return response.json();
    }

    _appendMessages(messages) {
        const fragment = document.createDocumentFragment();
        messages.forEach(message => {
            const messageElement = this._createMessageElement(message);
            fragment.appendChild(messageElement);
        });
        this.messagesContainer.appendChild(fragment);
    }

    _prependMessages(messages) {
        const fragment = document.createDocumentFragment();
        messages.reverse().forEach(message => {
            const messageElement = this._createMessageElement(message);
            fragment.insertBefore(messageElement, fragment.firstChild);
        });
        this.messagesContainer.insertBefore(fragment, this.messagesContainer.firstChild);
    }

    _createMessageElement(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', message.author === this.userUsername ? 'sent' : 'received');
        messageElement.setAttribute('data-id', message.id);

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
}