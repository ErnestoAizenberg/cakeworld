import { Chat } from './chat.js';

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed.');

    // Получаем контейнер сообщений
    const messagesContainer = document.getElementById('messages');
    if (!messagesContainer) {
        console.error('Messages container not found!');
        return;
    }
    console.log('Messages container found:', messagesContainer);

    // Получаем данные из атрибутов контейнера
    const chatId = messagesContainer.dataset.chatId;
    const userId = messagesContainer.dataset.userId;
    const userUsername = messagesContainer.dataset.userUsername;
    const chatUrlName = messagesContainer.dataset.chatUrlName;

    console.log('Data extracted from messages container:', {
        chatId,
        userId,
        userUsername,
        chatUrlName
    });

    // Проверяем, что все данные присутствуют
    if (!chatId || !userId || !userUsername || !chatUrlName) {
        console.error('Missing required data attributes!');
        return;
    }

    // Инициализируем чат
    console.log('Initializing Chat...');
    try {
        new Chat(chatId, userId, userUsername, chatUrlName);
        console.log('Chat initialized successfully.');
    } catch (error) {
        console.error('Error initializing Chat:', error);
    }
});