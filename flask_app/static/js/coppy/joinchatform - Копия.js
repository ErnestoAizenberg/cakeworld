document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('joinChatModal');
  const urlForRequest = modal.dataset.chatUrl; // Получаем значение из data-chat-url-name

  const openModal = () => modal.style.display = 'block';
  const closeModal = () => {
    modal.style.display = 'none';
    resetMessages();
  };

  const resetMessages = () => {
    document.getElementById('loadingMessage').style.display = 'none';
    document.getElementById('successMessage').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
  };

  const showLoading = () => {
    resetMessages();
    document.getElementById('loadingMessage').style.display = 'block';
  };

  const showSuccess = () => {
    resetMessages();
    document.getElementById('successMessage').style.display = 'block';
  };

  const showError = (message) => {
    resetMessages();
    document.getElementById('errorText').innerText = message;
    document.getElementById('errorMessage').style.display = 'block';
  };

  document.getElementById('openJoinModalButton').onclick = openModal;
  document.querySelector('.close').onclick = closeModal;

  window.onclick = (event) => {
    if (event.target === modal) {
      closeModal();
    }
  };

  document.getElementById('joinChatForm').onsubmit = async (event) => {
    event.preventDefault(); // предотвращаем обычное поведение формы

    showLoading();

    const reason = document.getElementById('reason').value;
    
    const csrfToken = document.getElementById('csrf-token').value;

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 секунд на ответ

      const response = await fetch(`${urlForRequest}`, {
        method: 'POST',
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ reason })
      });

      clearTimeout(timeoutId);

      if (response.ok) {
        showSuccess();
      } else {
        const errorData = await response.json();
        showError(errorData.message || 'Ошибка при отправке запроса. Попробуйте еще раз.');
      }
    } catch (err) {
      if (err.name === 'AbortError') {
        showError('Запрос занял слишком много времени. Попробуйте еще раз.');
      } else {
        showError('Произошла ошибка при отправке запроса. Попробуйте еще раз.');
      }
    }
  };

  document.getElementById('closeModal').onclick = closeModal;

  document.getElementById('retryRequest').onclick = () => {
    closeModal();
    openModal();
  };
});



