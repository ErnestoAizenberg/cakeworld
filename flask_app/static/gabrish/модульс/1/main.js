import { MessageLoader } from './messageLoader.js';
import { MessageSender } from './messageSender.js';
import { MessageViewTracker } from './messageViewTracker.js';

document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('messages');
    if (!messagesContainer) {
        console.error('Элемент с id="messages" не найден');
        return;
    }

    const chatId = messagesContainer.dataset.chatId;
    const userId = messagesContainer.dataset.userId;
    const limit = window.innerWidth <= 768 ? 20 : 50; // Лимит для мобильных и PC

    // Инициализация модулей
    const messageLoader = new MessageLoader(messagesContainer, chatId, userId, limit);
    const messageSender = new MessageSender('messageForm', chatId, userId);
    const messageViewTracker = new MessageViewTracker(messagesContainer, userId);

    messageLoader.loadInitialMessages();
    messageSender.init();
    messageViewTracker.init();

    // Обработчик прокрутки
    messagesContainer.addEventListener('scroll', () => {
        const { scrollTop, scrollHeight, clientHeight } = messagesContainer;

        if (scrollTop === 0) {
            messageLoader.loadOlderMessages();
        }

        if (scrollTop + clientHeight >= scrollHeight - 100) {
            messageLoader.loadNewerMessages();
        }
    });

    // Обработчик кнопки "↓" для прокрутки вниз
    const scrollToBottomButton = document.getElementById('scroll-to-bottom');
    if (scrollToBottomButton) {
        scrollToBottomButton.addEventListener('click', () => {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        });
    }
});