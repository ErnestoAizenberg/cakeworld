export class MessageLoader {
    constructor(messagesContainer, chatId, userId, limit) {
        if (!messagesContainer || !chatId || !userId || !limit) {
            throw new Error('MessageLoader: Missing required parameters');
        }

        this.messagesContainer = messagesContainer;
        this.chatId = chatId;
        this.userId = userId;
        this.limit = limit;
        this.offsetTop = 0;
        this.offsetBottom = 0;
        this.isLoading = false;

        console.log('MessageLoader initialized with:', {
            chatId: this.chatId,
            userId: this.userId,
            limit: this.limit
        });
    }


    
async loadInitialMessages() {
    console.log('Loading initial messages...');
    try {
        const data = await this._fetchMessages(this.offsetBottom, this.limit);
        console.log('Initial messages loaded:', data.messages);
        this._appendMessages(data.messages);
        this.offsetBottom += data.messages.length;
        console.log('OffsetBottom updated to:', this.offsetBottom);
    } catch (error) {
        console.error('Ошибка при загрузке сообщений:', error);
    }
}

async loadOlderMessages() {
    if (this.isLoading) {
        console.log('Older messages loading skipped: already loading.');
        return;
    }
    this.isLoading = true;
    console.log('Loading older messages...');

    try {
        const data = await this._fetchMessages(this.offsetTop, this.limit);
        console.log('Older messages loaded:', data.messages);
        this._prependMessages(data.messages);
        this.offsetTop += data.messages.length;
        console.log('OffsetTop updated to:', this.offsetTop);
    } catch (error) {
        console.error('Ошибка при загрузке старых сообщений:', error);
    } finally {
        this.isLoading = false;
        console.log('Older messages loading finished.');
    }
}

async loadNewerMessages() {
    if (this.isLoading) {
        console.log('Newer messages loading skipped: already loading.');
        return;
    }
    this.isLoading = true;
    console.log('Loading newer messages...');

    try {
        const data = await this._fetchMessages(this.offsetBottom, this.limit);
        console.log('Newer messages loaded:', data.messages);
        this._appendMessages(data.messages);
        this.offsetBottom += data.messages.length;
        console.log('OffsetBottom updated to:', this.offsetBottom);
    } catch (error) {
        console.error('Ошибка при загрузке новых сообщений:', error);
    } finally {
        this.isLoading = false;
        console.log('Newer messages loading finished.');
    }
}



    async loadOlderMessages() {
        if (this.isLoading) {
            console.log('Older messages loading skipped: already loading.');
            return;
        }
        this.isLoading = true;
        console.log('Loading older messages...');

        try {
            const data = await this._fetchMessages(this.offsetTop, this.limit);
            console.log('Older messages loaded:', data.messages);
            this._prependMessages(data.messages);
            this.offsetTop += data.messages.length;
            console.log('OffsetTop updated to:', this.offsetTop);
        } catch (error) {
            console.error('Ошибка при загрузке старых сообщений:', error);
        } finally {
            this.isLoading = false;
            console.log('Older messages loading finished.');
        }
    }

    async loadNewerMessages() {
        if (this.isLoading) {
            console.log('Newer messages loading skipped: already loading.');
            return;
        }
        this.isLoading = true;
        console.log('Loading newer messages...');

        try {
            const data = await this._fetchMessages(this.offsetBottom, this.limit);
            console.log('Newer messages loaded:', data.messages);
            this._appendMessages(data.messages);
            this.offsetBottom += data.messages.length;
            console.log('OffsetBottom updated to:', this.offsetBottom);
        } catch (error) {
            console.error('Ошибка при загрузке новых сообщений:', error);
        } finally {
            this.isLoading = false;
            console.log('Newer messages loading finished.');
        }
    }




async _fetchMessages(offset, limit) {
    console.log('Fetching messages with:', {
        chatId: this.chatId,
        userId: this.userId,
        offset,
        limit
    });

    const url = `/load-chat-messages-feed?chat_id=${this.chatId}&offset=${offset}&limit=${limit}&user_id=${this.userId}`;
    console.log('Fetching from URL:', url);

    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Ошибка сети или сервера: ${response.statusText}`);
    }

    const data = await response.json();
    console.log('Fetched data:', data);
    return data;
}


  
        const url = `/load-chat-messages-feed?chat_id=${this.chatId}&offset=${offset}&limit=${limit}&user_id=${this.userId}`;
        console.log('Fetching from URL:', url);

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Ошибка сети или сервера: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Fetched data:', data);
        return data;
    }

    _appendMessages(messages) {
        if (!messages || messages.length === 0) {
            console.log('No messages to append.');
            return;
        }

        console.log('Appending messages:', messages);
        const fragment = document.createDocumentFragment();
        messages.forEach(message => {
            const messageElement = this._createMessageElement(message);
            fragment.appendChild(messageElement);
        });
        this.messagesContainer.appendChild(fragment);
        console.log('Messages appended to container.');
    }

    _prependMessages(messages) {
        if (!messages || messages.length === 0) {
            console.log('No messages to prepend.');
            return;
        }

        console.log('Prepending messages:', messages);
        const fragment = document.createDocumentFragment();
        messages.reverse().forEach(message => {
            const messageElement = this._createMessageElement(message);
            fragment.insertBefore(messageElement, fragment.firstChild);
        });
        this.messagesContainer.insertBefore(fragment, this.messagesContainer.firstChild);
        console.log('Messages prepended to container.');
    }

    _createMessageElement(message) {
        console.log('Creating message element for:', message);
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', message.author === this.userId ? 'sent' : 'received');
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
                    ${message.is_viewed ? '<span>(Просмотрено)</span>' : ''}
                </div>
            </div>
        `;

        console.log('Message element created:', messageElement);
        return messageElement;
    }
}