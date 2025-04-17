export class MessageLoader {
    constructor({ messagesContainer, chatId, userId, limit }) {
        this.messagesContainer = messagesContainer; // Элемент DOM, куда будут добавлены сообщения
        this.chatId = chatId; // ID чата, для которого загружаются сообщения
        this.userId = userId; // ID пользователя, которому принадлежат сообщения
        this.limit = limit; // Лимит на количество загружаемых сообщений за один запрос
        this.offsetTop = 0; // Смещение для загрузки старых сообщений
        this.offsetBottom = 0; // Смещение для загрузки новых сообщений
        this.isLoading = false; // Флаг, показывающий, идет ли в данный момент загрузка сообщений
    }



    async loadInitialMessages() {
        try {
            const data = await this._fetchMessages(this.offsetBottom, this.limit, this.chatId, this.userId);
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
            const data = await this._fetchMessages(this.offsetTop, this.limit);
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
            const data = await this._fetchMessages(this.offsetBottom, this.limit);
            this._appendMessages(data.messages);
            this.offsetBottom += data.messages.length;
        } catch (error) {
            console.error('Ошибка при загрузке новых сообщений:', error);
        } finally {
            this.isLoading = false;
        }
    }

    async _fetchMessages(offset, limit, chatId, user_id) {
    const url = `/load-chat-messages-feed?chat_id=${chatId}&offset=${offset}&limit=${limit}&user_id=${user_id}`;
    
    console.debug('Запрос к API:', url); // Логирование запроса

    try {
        const response = await fetch(url);

        console.debug('Статус ответа:', response.status); // Логирование статуса ответа

        if (!response.ok) {
            const errorText = await response.text(); // Получаем текст ошибки с сервера
            console.error('Ошибка сети или сервера:', response.status, errorText); // Логируем ошибку
            throw new Error(`Ошибочный ответ ${response.status}: ${errorText}`);
        }

        const data = await response.json();
        console.debug('Полученные данные:', data); // Логирование полученных данных
        return data;

    } catch (error) {
        console.error('Ошибка при выполнении запроса:', error); // Логируем любую ошибку
        throw error; // Пробрасываем ошибку дальше
    }
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

    return messageElement;
}
}