import { Chat } from './chat.js';

document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('messages');
    if (!messagesContainer) return;

    const chatId = messagesContainer.dataset.chatId;
    const userId = messagesContainer.dataset.userId;
    const userUsername = messagesContainer.dataset.userUsername;
    const chatUrlName = messagesContainer.dataset.chatUrlName;

    new Chat(chatId, userId, userUsername, chatUrlName);
});