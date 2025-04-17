function toggleChatList() {
    const chatListDropdown = document.querySelector('.chat-list-dropdown');
    chatListDropdown.classList.toggle('show');
}


function showModal(url) { document.getElementById('modal-iframe').src = url; document.getElementById('modal').style.display = 'block'; } function closeModal() { document.getElementById('modal').style.display = 'none'; document.getElementById('modal-iframe').src = ''; // Очищаем URL iframe для предотвращения скрытого загрузки } function showProfile(element) { // Получаем URL - замените на ваш const url = 'https://example.com/profile'; showModal(url); } function showAvatarMenu(element, url) { // Вызываем функцию для отображения модального окна showModal(url); }


