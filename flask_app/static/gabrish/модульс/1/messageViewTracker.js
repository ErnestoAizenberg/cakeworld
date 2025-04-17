export class MessageViewTracker {
    constructor(messagesContainer, userId) {
        this.messagesContainer = messagesContainer;
        this.userId = userId;
    }

    init() {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const messageId = entry.target.dataset.id;
                        if (!entry.target.dataset.viewed) {
                            this._sendViewEvent(messageId);
                            entry.target.dataset.viewed = true;
                        }
                    }
                });
            },
            { threshold: 0.5 }
        );

        this.messagesContainer.querySelectorAll('.message').forEach(message => {
            observer.observe(message);
        });
    }

    async _sendViewEvent(messageId) {
        try {
            const response = await fetch(`/message/${messageId}/view`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: this.userId }),
            });

            if (!response.ok) {
                const text = await response.text();
                throw new Error(`Ошибка сервера: ${text}`);
            }

            const data = await response.json();
            console.log('Просмотр сообщения зарегистрирован:', data);
        } catch (error) {
            console.error('Ошибка при отправке события просмотра:', error);
        }
    }
}