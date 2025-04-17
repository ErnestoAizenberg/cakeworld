let isLoading = false; // Флаг для предотвращения множественных запросов
let offset = 0; 



function leaveChat() {
    // Emit a Socket.IO event to leave the chat
    socket.emit('leave', { username: '{{ user.username }}', room: '{{ chat.url_name }}' });

    // Redirect to the home page
    window.location.href = '/';
}

function toggleChatList() {
    const chatListDropdown = document.querySelector('.chat-list-dropdown');
    chatListDropdown.classList.toggle('show');
}

function loadMessages() {
    if (isLoading) return;
    isLoading = true;

    const loadingIndicator = document.getElementById('loadingIndicator');
    loadingIndicator.style.display = 'block';

    fetch(`/load_messages?chat_id={{ chat.id }}&offset=${offset}&limit=10`)
        .then(response => response.json())
        .then(data => {
            if (data.messages.length > 0) {
                const messagesContainer = document.getElementById('messages');
                data.messages.reverse().forEach(message => {
                    const messageElement = document.createElement('div');
                    messageElement.classList.add('message', message.author === '{{ user.username }}' ? 'sent' : 'received');
                    
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
                                <i class="fas fa-eye"></i> 0
                            </div>
                        </div>
                    `;
                    messagesContainer.insertBefore(messageElement, messagesContainer.firstChild);
                });

                offset += data.messages.length;
            }
            isLoading = false;
            loadingIndicator.style.display = 'none';
        })
        .catch(error => {
            console.error('Error loading messages:', error);
            isLoading = false;
            loadingIndicator.style.display = 'none';
        });
}

// Загружаем последние сообщения при загрузке страницы
loadMessages();





const messagesContainer = document.getElementById('messages');
messagesContainer.addEventListener('scroll', () => {
    if (messagesContainer.scrollTop === 0) {
        loadMessages(); // Подгружаем сообщения при прокрутке вверх
    }
});





         
  const socket = io();

  // Join the chat room
  socket.emit('join', { username: '{{ user.username }}', room: '{{ chat.url_name }}' });

  // Listen for new messages
  socket.on('new_message', (data) => {
    const messages = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', data.author === '{{ user.username }}' ? 'sent' : 'received');
    messageElement.innerHTML = `
      <div class="message-content">
        <span style="color:blue;">${data.author}:</span>
        ${data.text}
        <div class="message-info">
          <span>${data.created}</span>
          <i class="fas fa-eye"></i> 0
        </div>
      </div>
    `;
    messages.appendChild(messageElement);
    messages.scrollTop = messages.scrollHeight; // Auto-scroll to the latest message
  });

  // Handle message submission
  document.getElementById('messageForm').addEventListener('submit', (e) => {
  e.preventDefault();

  const messageInput = document.getElementById('messageInput');
  const message = messageInput.value.trim();
  const imageInput = document.getElementById('imageInput');
  const formData = new FormData();

  // Добавляем текстовое сообщение
  formData.append('user_id', '{{ user.id }}');
  formData.append('chat_id', '{{ chat.id }}');
  formData.append('message', message);

  // Добавляем изображения
  const files = imageInput.files;
  for (let i = 0; i < files.length; i++) {
    formData.append('images', files[i]);
  }

  // Логируем FormData
  for (let [key, value] of formData.entries()) {
    console.log(key, value);
  }

  // Отправляем данные на сервер
  fetch('/submit_message', {
    method: 'POST',
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        // Логируем статус и тело ответа
        console.error('Server returned:', response.status, response.statusText);
        return response.text().then(text => {
          console.error('Response body:', text);
          throw new Error('Failed to send message');
        });
      }
      return response.json();
    })
    .then((data) => {
      if (data.status === 'success') {
        messageInput.value = ''; // Очищаем текстовое поле
        imageInput.value = ''; // Очищаем поле выбора файла
        imagePreviews.innerHTML = ''; // Очищаем предпросмотр изображений
      } else {
        alert('Error: ' + data.error);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      alert('Failed to send message. Please try again.');
    });
});

socket.on('new_message', (data) => {
    const messages = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', data.author === '{{ user.username }}' ? 'sent' : 'received');
    
    const imagesHTML = data.image_urls && data.image_urls.length > 0 
        ? `<div class="message-images">
             ${data.image_urls.map(url => `<img src="${url}" alt="Attached Image">`).join('')}
           </div>`
        : '';

    messageElement.innerHTML = `
        <div class="message-content">
            <span style="color:blue;">${data.author}:</span>
            ${data.text}
            ${imagesHTML}
            <div class="message-info">
                <span>${data.created}</span>
                <i class="fas fa-eye"></i> 0
            </div>
        </div>
    `;
    
    messages.appendChild(messageElement);
    messages.scrollTop = messages.scrollHeight; // Автоматическая прокрутка к новому сообщению
});


