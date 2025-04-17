export class MessageSender {
    constructor(formId, chatId, userId) {
        this.form = document.getElementById(formId);
        this.chatId = chatId;
        this.userId = userId;
    }

    init() {
        this.form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this._sendMessage();
        });
    }

    async _sendMessage() {
        const formData = new FormData(this.form);
        formData.append('chat_id', this.chatId);
        formData.append('user_id', this.userId);

        try {
            const response = await fetch('/submit_message', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const text = await response.text();
                throw new Error(`Ошибка сервера: ${text}`);
            }

            const data = await response.json();
            if (data.status === 'success') {
                this._clearForm();
                this._showNotification('Сообщение отправлено успешно!', 'success');
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Ошибка при отправке сообщения:', error);
            this._showNotification('Не удалось отправить сообщение. Пожалуйста, попробуйте еще раз.', 'error');
        }
    }

    _clearForm() {
        this.form.reset();
        const imagePreviews = this.form.querySelector('.image-previews');
        if (imagePreviews) imagePreviews.innerHTML = '';
    }

    _showNotification(message, status) {
        const notification = document.createElement('div');
        notification.className = `notification ${status}-notification`;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 2000);
    }
}