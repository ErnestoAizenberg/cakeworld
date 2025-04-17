export class MessageViewTracker {
    constructor(messagesContainer, userId) {
        this.messagesContainer = messagesContainer;
        this.userId = userId;
        this.observer = null;
    }

    init() {
        // Создаем новый IntersectionObserver
        this.observer = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const messageId = entry.target.dataset.id;

                        if (!entry.target.dataset.viewed) {
                            this._sendViewEvent(messageId);
                            entry.target.dataset.viewed = true; // Пометить как просмотренное
                        }
                    }
                });
            },
            { threshold: 0.5 } // Соответствует более чем 50% видимости
        );

        // Наблюдение за существующими сообщениями
        this._observeMessages();
    }

    _observeMessages() {
        this.messagesContainer.querySelectorAll('.message').forEach(message => {
            this.observer.observe(message);
        });
    }

    async _sendViewEvent(messageId) {
        try {
            const response = await fetch(`/view_direct_message/${messageId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: this.userId }),
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Ошибка сервера: ${errorText}`);
            }

            const data = await response.json();
            console.log('Просмотр сообщения зарегистрирован:', data);
        } catch (error) {
            console.error('Ошибка при отправке события просмотра:', error);
        }
    }

    // Метод для добавления нового сообщения
    addMessage(message) {
        const messageElement = this._createMessageElement(message);
        this.messagesContainer.appendChild(messageElement);
        // Начнем наблюдение за новым сообщением
        this.observer.observe(messageElement);
    }

    // Creating HTML element for a message
_createMessageElement(message) {
    const messageElement = document.createElement('div');
    
    // Определяем класс для сообщения (sent или received)
    const messageClass = message.user_id === this.userId ? 'sent' : 'received';
    messageElement.classList.add('message', messageClass);
    messageElement.setAttribute('data-id', message.id);

    // Отладочная информация
    console.log(`Creating message element: ${message.text} (User ID: ${message.user_id}, Is own: ${message.user_id === this.userId})`);

    // Определяем класс для содержимого сообщения (user или other)
    const contentClass = (message.user_id === this.userId ? 'user' : 'other');
    
    messageElement.innerHTML = `
    <div class="message">
        <div class="message-content ${contentClass}">
            <p>${message.text}</p>
            <span class="timestamp">${message.created}</span>${message.is_read ? '<span>(Viewed)</span>' : ''}
        </div>    
    </div>`;

    // Отладочная информация о добавленных классах
    console.log(`Message class: ${messageClass}, Content class: ${contentClass}`);

    return messageElement;
}

}