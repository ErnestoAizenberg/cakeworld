import { Chat } from './direct_chat.js';

document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('messages');
    if (!messagesContainer) return;

    const { chatId, userId, ownerId, userUsername, chatUrlName } = messagesContainer.dataset;

    new Chat({
        messagesContainer,
        chatId,
        userId,
        ownerId,
        userUsername,
        chatUrlName
    });
});